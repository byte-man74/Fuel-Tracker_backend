from django import forms
from .models import Fueling_station, Fuel_Station_Position, Fuel_Station_Price
from django.contrib.auth.forms import UserCreationForm
from Auth.models import CustomUser

class FuelingStationForm(forms.ModelForm):
    class Meta:
        model = Fueling_station
        fields = ['name', 'address', 'local_government']

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class FuelingStationPositionForm (forms.ModelForm):
    class Meta:
        model = Fuel_Station_Position
        fields = ["longitude", "latitude"]

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

class FuelStationPriceForm(forms.ModelForm):
    class Meta:
        model = Fuel_Station_Price
        fields = ['amount',]
        labels = {
            'amount': 'Fuel Price Amount per Litre',
        }