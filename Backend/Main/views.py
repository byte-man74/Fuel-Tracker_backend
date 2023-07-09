from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import FuelingStationForm, FuelingStationPositionForm
from .models import Fueling_station, Fuel_Station_Position, Images_on_station
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .forms import SignupForm

from django.db.models import Q

# ...
def landing_page (request):
    return render (request, 'main/landing_page.html')

def sign_up (request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Replace 'home' with the URL name of your home page
    else:
        form = SignupForm()
    return render (request, 'main/sign_up.html', {'form': form}) 


def login_page (request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Replace 'dashboard' with the desired URL for authenticated users
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render (request, 'main/login.html', {'form': form})


def create_fueling_station(request):
    if request.method == 'POST':
        form = FuelingStationForm(request.POST)
        if form.is_valid():
            fueling_station = form.save(commit=False)  # Save the form data but don't commit to the database yet
            fueling_station_name = form.cleaned_data.get('name')  # Get the name from the form data
            
            try:
                image_on_station = Images_on_station.objects.get(station_name=fueling_station_name)
                fueling_station.logo_url = image_on_station.station_logo.url
                fueling_station.background_image_url = image_on_station.station_background.url
            except Images_on_station.DoesNotExist:
                # Set default values for logo_url and background_image_url
                fueling_station.logo_url = 'default_logo_url'
                fueling_station.background_image_url = 'default_background_image_url'
            
            fueling_station.save()  # Save the fueling_station object to the database
            messages.success(request, 'Fueling station has been successfully added to the database. Please provide more information about the location.')
            return redirect('Fuel station position', fueling_station_id=fueling_station.id)
    else:
        form = FuelingStationForm()
    
    return render(request, 'main/form.html', {'form': form})

from django.db import IntegrityError

def fuel_station_position(request, fueling_station_id):
    station = Fueling_station.objects.get(id=fueling_station_id)
    try:
        fueling_station_position = Fuel_Station_Position.objects.get(station=station)
    except Fuel_Station_Position.DoesNotExist:
        fueling_station_position = None

    if request.method == "POST":
        form = FuelingStationPositionForm(request.POST, instance=fueling_station_position)
        if form.is_valid():
            fueling_station_position = form.save(commit=False)
            fueling_station_position.station = station
            fueling_station_position.save()
            messages.success(request, 'Fueling station location information has been added succesfully.')
            return redirect("success_okay")
    else:
        form = FuelingStationPositionForm(instance=fueling_station_position)

    return render(request, 'main/form.html', {'form': form, 'fueling_station_id': fueling_station_id})

def dashboard (request):
    stations = Fueling_station.objects.all().prefetch_related('fuel_station_price')

    return render(request, 'main/dashboard.html', {'stations': stations})

def success (request):
    return render(request, 'main/success.html')