from .models import Walk
from django import forms
from django.utils.dateparse import parse_duration


class DateTimeInput(forms.widgets.DateTimeInput):
    input_type = 'datetime-local'


class WalkForm(forms.ModelForm):

    class Meta:
        model = Walk
        fields = ('start_time', 'location', 'duration', 'distance', 'actual_distance', 'active_kilocalories', 'total_kilocalories', 'elevation_gain', 'average_heart_rate')

        widgets = {
            'start_time': DateTimeInput(),
            'duration': forms.TextInput(attrs={"class": "html-duration-picker"}),
        }
