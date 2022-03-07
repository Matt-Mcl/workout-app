from .models import *
from django import forms


class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        
        fields = ('name', 'location', 'start_time', 'duration', 'active_kilocalories', 'total_kilocalories', 'average_heart_rate', 'max_heart_rate', 'distance', 'actual_distance', 'elevation_gain', 'step_cadence', 'temperature', 'humidity', 'intensity', 'flights_climbed', 'step_count', 'swim_cadence', 'total_swimming_stroke_count', 'notes')

        widgets = {
            'start_time': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M:%S'), attrs={'type': 'datetime-local'}),
            'duration': forms.TextInput(attrs={"class": "html-duration-picker"}),
        }
