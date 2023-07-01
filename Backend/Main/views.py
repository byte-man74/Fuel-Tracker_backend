from django.shortcuts import render, redirect
from .forms import FuelingStationForm

def create_fueling_station(request):
    if request.method == 'POST':
        form = FuelingStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fueling_station_list')  # Redirect to a success page
    else:
        form = FuelingStationForm()
    
    return render(request, 'main/form.html', {'form': form})
