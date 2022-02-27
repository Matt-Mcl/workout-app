from rest_framework import serializers

from .models import Walk, Run

class WalkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Walk
        fields = ('location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'elevation_gain', 'total_kilocalories', 'average_heart_rate')

class RunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Run
        fields = ('location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'elevation_gain', 'total_kilocalories', 'average_heart_rate', 'average_cadence')

