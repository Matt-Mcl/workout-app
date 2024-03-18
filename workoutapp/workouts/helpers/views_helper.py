from rest_framework_api_key.models import APIKey
from ..models import User
from datetime import datetime, timedelta


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
        location = "O"
        if w['location'] == "Indoor":
            location = "I"

        start = datetime.strptime(w['start'], "%Y-%m-%d %H:%M:%S %z")
        end = datetime.strptime(w['end'], "%Y-%m-%d %H:%M:%S %z")
        duration = timedelta(seconds=int(w['duration']))

        activeEnergy = int(sum(ae['qty'] for ae in w['activeEnergy']))

        minsAtHRs = {}
        cumulativeAverageHR = 0
        HRSamples = 0
        maxHR = 0

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

        totalDistance = 0

        if "distance" in w:
            totalDistance = round(w['distance']['qty'], 2)
            
        totalSteps = 0
        
        for item in w['stepCount']:
            totalSteps += item['qty']

        stepCadence = int(totalSteps / (w['duration'] / 60))

        obj = {
            "name": w['name'],
            "location": location,
            "start_time": start,
            "end_time": end,
            "duration": duration,
            "active_kilocalories": activeEnergy,
            "average_heart_rate": round(cumulativeAverageHR/HRSamples),
            "max_heart_rate": maxHR,
            "mins_at_hr": str(minsAtHRs),
            "distance": totalDistance,
            "step_count": round(totalSteps),
            "step_cadence": stepCadence,
            "temperature": int(w['temperature']['qty']),
            "humidity": int(w['humidity']['qty']),
            "intensity": round(w['intensity']['qty'], 2),
            "user": user_id
        }

        print(obj['name'], obj['duration'], flush=True)

        workout_objects.append(obj)

    return workout_objects
