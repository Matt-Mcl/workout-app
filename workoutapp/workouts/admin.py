from django.contrib import admin

from .models import Workout


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'duration', 'distance']
