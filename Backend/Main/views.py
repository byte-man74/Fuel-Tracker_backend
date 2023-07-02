from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import FuelingStationForm, FuelingStationPositionForm


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


def fuel_station_position(request, fueling_station_id):
    if request.method == "POST":
        form = FuelingStationPositionForm(request.POST)
        if form.is_valid():
            fueling_station_position = form.save(commit=False)
            fueling_station_position.station = fueling_station_id
            fueling_station_position.save()
            return redirect("success")
    else:
        form = FuelingStationPositionForm()

    return render(request, 'main/form.html', {'form': form, 'fueling_station_id': fueling_station_id})
