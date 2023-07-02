from django.contrib import messages
from django.shortcuts import redirect
from .forms import FuelingStationForm


def create_fueling_station(request):
    if request.method == 'POST':
        form = FuelingStationForm(request.POST)
        if form.is_valid():
            fueling_station = form.save()
            messages.success(request, 'Fueling station created successfully.')
            return redirect('fueling_station_detail', fueling_station_id=fueling_station.id)
    else:
        form = FuelingStationForm()
    
    return render(request, 'main/form.html', {'form': form})
