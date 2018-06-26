from django import forms
from .models import Setting


class ControllerForm(forms.Form):
    bedroom_target_temperature = forms.IntegerField(min_value=16, max_value=50)
    hot_water_target_temperature = forms.IntegerField(min_value=24, max_value=90)
    bedroom_light = forms.BooleanField(required=False)
    bathroom_light = forms.BooleanField(required=False)

    def save(self):
        pass
