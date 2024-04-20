from rest_framework import serializers
from rest_framework_api_key.models import APIKey

from .models import Workout, VO2Reading, User


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('name', 'location', 'start_time', 'end_time', 'duration', 'active_kilocalories', 'average_heart_rate', 'max_heart_rate', 'mins_at_hr', 'route', 'distance', 'actual_distance', 'step_count', 'step_cadence', 'temperature', 'humidity', 'intensity', 'notes', 'user')


class VO2ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VO2Reading
        fields = ('vo2_max', 'date', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'groups')


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ('prefix', 'name', 'revoked', 'expiry_date')
