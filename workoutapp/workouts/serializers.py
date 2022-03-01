from rest_framework import serializers

from .models import Walk, Run, User


class WalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walk
        fields = ('start_time', 'location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'elevation_gain', 'total_kilocalories', 'average_heart_rate', 'user')


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ('start_time', 'location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'elevation_gain', 'total_kilocalories', 'average_heart_rate', 'average_cadence', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'groups')

