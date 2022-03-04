from rest_framework_api_key.models import APIKey
from ..models import User
from datetime import datetime


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
        if w['isIndoor']:
            location = "I"

        start = datetime.strptime(w['start'], "%Y-%m-%d %H:%M:%S %z")
        end = datetime.strptime(w['end'], "%Y-%m-%d %H:%M:%S %z")
        duration = end - start

        object = {
            "name": w['name'],
            "location": location,
            "start_time": start,
            "duration": duration,
            "active_kilocalories": int(w['activeEnergy']['qty']),
            "total_kilocalories": int(w['totalEnergy']['qty']),
            "average_heart_rate": int(w['avgHeartRate']['qty']),
            "max_heart_rate": int(w['maxHeartRate']['qty']),
            "distance": round(w['distance']['qty'], 2),
            "elevation_gain": int(w['elevation']['ascent']),
            "step_cadence": int(w['stepCadence']['qty']),
            "temperature": int(w['temperature']['qty']),
            "humidity": int(w['humidity']['qty']),
            "intensity": round(w['intensity']['qty'], 2),
            "flights_climbed": int(w['flightsClimbed']['qty']),
            "step_count": int(w['stepCount']['qty']),
            "swim_cadence": int(w['intensity']['qty']),
            "total_swimming_stroke_count": int(w['intensity']['qty']),
            "user": user_id
        }

        workout_objects.append(object)

    return workout_objects
