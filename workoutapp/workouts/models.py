from django.db import models
from django.contrib.auth.models import User


class Walk(models.Model):
    LOCATION_CHOICES = [
        ('O', 'Outdoor'),
        ('I', 'Indoor')
    ]
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    actual_distance = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    active_kilocalories = models.IntegerField()
    elevation_gain = models.IntegerField(null=True)
    total_kilocalories = models.IntegerField()
    average_heart_rate = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Run(models.Model):
    LOCATION_CHOICES = [
        ('O', 'Outdoor'),
        ('I', 'Indoor')
    ]
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    actual_distance = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    active_kilocalories = models.IntegerField()
    elevation_gain = models.IntegerField(null=True)
    total_kilocalories = models.IntegerField()
    average_heart_rate = models.IntegerField()
    average_cadence = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
