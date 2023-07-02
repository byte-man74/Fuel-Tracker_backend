from django import forms
from .models import Fueling_station, Fuel_Station_Position

class FuelingStationForm(forms.ModelForm):
    class Meta:
        model = Fueling_station
        fields = ['name', 'address', 'local_government']


class FuelingStationPositionForm (forms.ModelForm):
    class Meta:
        model = Fuel_Station_Position
        fields = ["longitude", "latitude"]