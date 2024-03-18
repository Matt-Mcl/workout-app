from .models import *
from django import forms


class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        
        fields = ('name', 'location', 'start_time', 'end_time', 'duration', 'active_kilocalories', 'average_heart_rate', 'max_heart_rate', 'distance', 'actual_distance', 'step_count', 'step_cadence', 'temperature', 'humidity', 'intensity', 'notes')

        widgets = {
            'start_time': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            'duration': forms.TextInput(attrs={"class": "html-duration-picker"}),
        }
