from rest_framework import serializers
from rest_framework_api_key.models import APIKey

from .models import Workout, User


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('name', 'location', 'start_time', 'duration', 'active_kilocalories', 'total_kilocalories', 'average_heart_rate', 'max_heart_rate', 'distance', 'actual_distance', 'elevation_gain', 'step_cadence', 'temperature', 'humidity', 'intensity', 'flights_climbed', 'step_count', 'swim_cadence', 'total_swimming_stroke_count', 'notes', 'user')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'groups')


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ('prefix', 'name', 'revoked', 'expiry_date')
