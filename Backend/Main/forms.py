from django import forms
from .models import Fueling_station

class FuelingStationForm(forms.ModelForm):
    class Meta:
        model = Fueling_station
        fields = ['name', 'address', 'local_government']
