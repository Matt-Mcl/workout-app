from .models import *
from django import forms


class WalkForm(forms.ModelForm):

    class Meta:
        model = Walk
        
        fields = ('start_time', 'location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'total_kilocalories', 'elevation_gain', 'average_heart_rate')

        widgets = {
            'start_time': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            'duration': forms.TextInput(attrs={"class": "html-duration-picker"}),
        }

class RunForm(forms.ModelForm):

    class Meta:
        model = Run
        
        fields = ('start_time', 'location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'total_kilocalories', 'elevation_gain', 'average_heart_rate', 'average_cadence')

        widgets = {
            'start_time': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            'duration': forms.TextInput(attrs={"class": "html-duration-picker"}),
        }
