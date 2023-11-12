from django.db import models
from django.contrib.auth.models import User

class StrengthExercise(models.Model):
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
    duration = models.IntegerField()
    moves = models.IntegerField()

    exercises = models.ManyToManyField(StrengthExercise)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
