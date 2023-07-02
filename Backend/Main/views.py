from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FuelingStationForm

def create_fueling_station(request):
    if request.method == 'POST':
        form = FuelingStationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fueling station created successfully.')
            return redirect('create_fueling_station')  # Redirect to the same page
    else:
        form = FuelingStationForm()
    
    return render(request, 'main/form.html', {'form': form})


