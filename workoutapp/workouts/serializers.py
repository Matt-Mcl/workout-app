from rest_framework import serializers

from .models import Walk, Run, User


class WalkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Walk
        fields = ('start_time', 'location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'elevation_gain', 'total_kilocalories', 'average_heart_rate', 'user')


class RunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Run
        fields = ('start_time', 'location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'elevation_gain', 'total_kilocalories', 'average_heart_rate', 'average_cadence', 'user')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

