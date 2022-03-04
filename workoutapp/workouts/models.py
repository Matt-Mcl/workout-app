from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    LOCATION_CHOICES = [
        ('O', 'Outdoor'),
        ('I', 'Indoor')
    ]
    location = models.CharField(null=True, blank=True, max_length=1, choices=LOCATION_CHOICES)
    start_time = models.DateTimeField(unique=True)
    duration = models.DurationField()
    active_kilocalories = models.IntegerField()
    total_kilocalories = models.IntegerField()
    average_heart_rate = models.IntegerField()
    max_heart_rate = models.IntegerField()
    distance = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    actual_distance = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    elevation_gain = models.IntegerField(null=True, blank=True)
    step_cadence = models.IntegerField(null=True, blank=True)
    temperature = models.IntegerField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    intensity = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    flights_climbed = models.IntegerField(null=True, blank=True)
    step_count = models.IntegerField(null=True, blank=True)
    swim_cadence = models.IntegerField(null=True, blank=True)
    total_swimming_stroke_count = models.IntegerField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
