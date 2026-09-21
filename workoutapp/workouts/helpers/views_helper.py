from rest_framework_api_key.models import APIKey
import math
from ..models import User, Workout, VO2Reading
from datetime import datetime, timedelta
from django.utils import timezone


def get_user_data(request):
    user = None
    # Check if key in headers
    if "HTTP_API_KEY" in request.META:
        # Get key value and then name of owner
        key = request.META["HTTP_API_KEY"]
        user_name = APIKey.objects.get_from_key(key)
        user = User.objects.filter(username=user_name)
    else:
        # Else just pull the user from the db
        user = User.objects.filter(id=request.user.id)

    return user


def parse_json_data(request, user_id):
    workout_objects = []

    workouts = request.data['data']['workouts']

    for w in workouts:
        start = datetime.strptime(w['start'], "%Y-%m-%d %H:%M:%S %z")
        end = datetime.strptime(w['end'], "%Y-%m-%d %H:%M:%S %z")
        duration = timedelta(seconds=int(w['duration']))

        print(w['name'], start, flush=True)

        location = "I"
        if "location" in w and w['location'] == "Outdoor":
            location = "O"

        activeEnergy = 0 
        if "activeEnergy" in w:
            if isinstance(w['activeEnergy'], list):
                activeEnergy = int(sum(ae['qty'] for ae in w['activeEnergy']))
            else:
                activeEnergy = int(w['activeEnergy']['qty'])

        minsAtHRs = {}
        cumulativeAverageHR = 0
        HRSamples = 0
        maxHR = 0
        avgHR = 0

        if "heartRateData" in w:
            for item in w['heartRateData']:
                HRSamples += 1
                averageHeartRate = round(item['Avg']) 
                cumulativeAverageHR += averageHeartRate

                if averageHeartRate in minsAtHRs:
                    minsAtHRs[averageHeartRate] += 1
                else:
                    minsAtHRs[averageHeartRate] = 1

                if round(item['Max']) > maxHR:
                    maxHR = round(item['Max'])

            minsAtHRs = sorted(minsAtHRs.items())
            avgHR = round(cumulativeAverageHR/HRSamples)

        route = []

        if "route" in w:
            # Only keep every 5th point to save on storage
            for item in w['route'][::5]:
                route.append((round(item['latitude'], 6), round(item['longitude'], 6)))

        totalDistance = 0

        if "distance" in w:
            totalDistance = round(w['distance']['qty'], 2)
            
        totalSteps = 0
        
        if "stepCount" in w:
            for item in w['stepCount']:
                totalSteps += item['qty']

        stepCadence = int(totalSteps / (w['duration'] / 60))

        temperature = None
        if "temperature" in w:
            temperature = int(w['temperature']['qty'])

        humidity = None
        if "humidity" in w:
            humidity = int(w['humidity']['qty'])

        intensity = None
        if "intensity" in w:
            intensity = round(w['intensity']['qty'], 2)

        obj = {
            "name": w['name'],
            "location": location,
            "start_time": start,
            "end_time": end,
            "duration": duration,
            "active_kilocalories": activeEnergy,
            "average_heart_rate": avgHR,
            "max_heart_rate": maxHR,
            "mins_at_hr": str(minsAtHRs),
            "route": str(route),
            "distance": totalDistance,
            "step_count": round(totalSteps),
            "step_cadence": stepCadence,
            "temperature": temperature,
            "humidity": humidity,
            "intensity": intensity,
            "user": user_id
        }

        workout_objects.append(obj)

    return workout_objects


def add_fitness_mins(workouts, user_id):
    # TODO: Modify to get the fitness mins threshold from user settings
    threshold = 138

    for w in workouts:
        # Get minutes of workout where heartrate is above threshold
        if w.mins_at_hr is not None:
            fitness_mins = sum([x[1] for x in eval(w.mins_at_hr) if int(x[0]) >= threshold])
            w.fitness_mins = fitness_mins

    return workouts


def get_week_fitness_mins(user_id, offset=0):
    # Get the workouts for the current week (monday to sunday) with timezone but from midnight
    start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=timezone.now().weekday()) - timedelta(days=offset*7)
    end_date = start_date + timedelta(days=7)

    workouts = Workout.objects.filter(user=user_id, start_time__gte=start_date, start_time__lte=end_date)

    workouts_with_fitness_mins = add_fitness_mins(workouts, user_id)

    # Sum the fitness mins
    total_fitness_mins = sum([w.fitness_mins for w in workouts_with_fitness_mins])

    return (total_fitness_mins, start_date, end_date)


# A reading older than this is called out as stale on the fitness page
STALE_VO2_DAYS = 42


def format_vo2_reading(reading):
    return {
        "value": round(reading.vo2_max, 1),
        "date": reading.date.strftime("%d/%m/%Y")
    }


def get_vo2_stats(user):
    # Every reading for the user, newest first
    readings = list(VO2Reading.objects.filter(user=user).order_by("-date"))

    if not readings:
        return None

    values = [r.vo2_max for r in readings]
    highest_value = max(values)
    lowest_value = min(values)

    # Where the same value was hit more than once, report when it was first achieved
    highest = min([r for r in readings if r.vo2_max == highest_value], key=lambda r: r.date)
    lowest = min([r for r in readings if r.vo2_max == lowest_value], key=lambda r: r.date)

    latest = readings[0]
    earliest = readings[-1]

    change = round(latest.vo2_max - earliest.vo2_max, 1)

    # The graph carries the last reading forward, so flag a reading that has gone stale
    days_since_latest = (timezone.localdate() - latest.date).days

    stats = {
        "latest": format_vo2_reading(latest),
        "days_since_latest": days_since_latest,
        "is_stale": days_since_latest > STALE_VO2_DAYS,
        "highest": format_vo2_reading(highest),
        "lowest": format_vo2_reading(lowest),
        "average": round(sum(values) / len(values), 1),
        "change": change,
        "change_display": "{}{}".format("+" if change > 0 else "", change),
        "first_date": earliest.date.strftime("%d/%m/%Y"),
        "readings": len(readings)
    }

    return stats


def get_vo2_axis_range(graph_fitness_mins, padding=3):
    # Fit the axis to the values plotted rather than a fixed range, so small changes are visible
    values = [item['vo2_max'] for item in graph_fitness_mins if item['vo2_max']]

    if not values:
        return {"min": 30, "max": 70}

    return {
        "min": int(math.floor(min(values))) - padding,
        "max": int(math.ceil(max(values))) + padding
    }
