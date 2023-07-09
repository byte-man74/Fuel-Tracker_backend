from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import FuelingStationForm, FuelingStationPositionForm
from .models import Fueling_station, Fuel_Station_Position, Images_on_station


from django.db.models import Q

# ...
def landing_page (request):
    return render (request, 'main/landing_page.html')

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
    
    return render(request, 'main/landing_page.html', {'form': form})

def sign_up (request):
    return render (request, 'main/sign_up.html') 

def login_page (request):
    return render (request, 'main/login.html')


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



def success (request):
    return render(request, 'main/success.html')