from django.db import models

# Create your models here.

class Walk(models.Model):
    LOCATION_CHOICES = [
        ('O', 'Outdoor'),
        ('I', 'Indoor')
    ]
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    duration = models.DurationField()
    distance = models.DecimalField()
    active_kilocalories = models.IntegerField()
    elevation_gain = models.IntegerField(blank=True)
    total_kilocalories = models.IntegerField()
    average_heart_rate = models.IntegerField()

class Run(models.Model):
    LOCATION_CHOICES = [
        ('O', 'Outdoor'),
        ('I', 'Indoor')
    ]
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    duration = models.DurationField()
    distance = models.DecimalField()
    active_kilocalories = models.IntegerField()
    elevation_gain = models.IntegerField(blank=True))
    total_kilocalories = models.IntegerField()
    average_heart_rate = models.IntegerField()
    average_cadence = models.IntegerField()
