from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    LOCATION_CHOICES = [
        ('O', 'Outdoor'),
        ('I', 'Indoor')
    ]
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    start_time = models.DateTimeField(unique=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField()
    active_kilocalories = models.IntegerField()
    average_heart_rate = models.IntegerField()
    max_heart_rate = models.IntegerField()
    mins_at_hr = models.TextField(null=True, blank=True)
    route = models.TextField(null=True, blank=True)
    distance = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    actual_distance = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    step_count = models.IntegerField(null=True, blank=True)
    step_cadence = models.IntegerField(null=True, blank=True)
    temperature = models.IntegerField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    intensity = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    notes = models.TextField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class VO2Reading(models.Model):
    vo2_max = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
