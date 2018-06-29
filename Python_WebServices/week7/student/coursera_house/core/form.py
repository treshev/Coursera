from django import forms
from .models import Setting


class ControllerForm(forms.Form):
    bedroom_target_temperature = forms.IntegerField(min_value=16, max_value=50)
    hot_water_target_temperature = forms.IntegerField(min_value=24, max_value=90)
    bedroom_light = forms.BooleanField(required=False)
    bathroom_light = forms.BooleanField(required=False)

    def save(self):
        bedroom_target_temperature = Setting.objects.get(controller_name='bedroom_target_temperature')
        bedroom_target_temperature.value = self.cleaned_data["bedroom_target_temperature"]
        bedroom_target_temperature.save()

        hot_water_target_temperature = Setting.objects.get(controller_name='hot_water_target_temperature')
        hot_water_target_temperature.value = self.cleaned_data["hot_water_target_temperature"]
        hot_water_target_temperature.save()

    def clean(self):
        return super().clean()
