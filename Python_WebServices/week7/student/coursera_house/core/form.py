from django import forms
from .models import Setting


class ControllerForm(forms.Form):
    bedroom_target_temperature = forms.IntegerField(min_value=16, max_value=50)
    hot_water_target_temperature = forms.IntegerField(min_value=24, max_value=90)
    bedroom_light = forms.BooleanField()
    bathroom_light = forms.BooleanField()

    def save(self):
        pass

    def load(self):
        self.data['bedroom_target_temperature'] = ['30']
        self.data['hot_water_target_temperature'] = 30

        self.data['bedroom_light'] = True
        self.data['bathroom_light'] = False
        print('ALTR I am in load')
