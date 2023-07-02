from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import FuelingStationForm, FuelingStationPositionForm
from .models import Fueling_station, Fuel_Station_Position


def create_fueling_station(request):
    if request.method == 'POST':
        form = FuelingStationForm(request.POST)
        if form.is_valid():
            fueling_station = form.save()
            messages.success(request, 'Fueling station has been successfully added to the database please provide more information about the location.')
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
            return redirect("success_okay")
    else:
        form = FuelingStationPositionForm(instance=fueling_station_position)

    return render(request, 'main/form.html', {'form': form, 'fueling_station_id': fueling_station_id})



def success (request):
    return render(request, 'main/success.html')