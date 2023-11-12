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
    notes = models.TextField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class StrengthExercise(models.Model):
    # Execises contains a name, sets, reps to do, reps done, kg to do and kg done per StrengthWorkout
    name = models.CharField(max_length=100)
    set = models.IntegerField()
    reps_to_do = models.CharField(max_length=10)
    reps_done = models.CharField(max_length=10)
    kg_to_do = models.CharField(max_length=10)
    kg_done = models.CharField(max_length=10)


class StrengthWorkout(models.Model):
    date = models.DateTimeField(unique=True)
    intensity_string = models.CharField(max_length=100)
    intensity = models.IntegerField()
    duration = models.DurationField()
    moves = models.IntegerField()

    exercises = models.ManyToManyField(StrengthExercise)
