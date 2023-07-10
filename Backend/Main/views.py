from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .forms import FuelingStationForm, LoginForm, SignupForm
from .models import Fueling_station, Fuel_Station_Position, Images_on_station
from django.shortcuts import get_object_or_404

def landing_page(request):
    return render(request, 'main/landing_page.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'main/sign_up.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})



def create_fueling_station(request):
    if request.method == 'POST':
        form = FuelingStationForm(request.POST)
        if form.is_valid():
            fueling_station = form.save(commit=False)
            fueling_station.save()

            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')

            station = get_object_or_404(Fueling_station, id=fueling_station.id)
            position_object, created = Fuel_Station_Position.objects.get_or_create(
                station=station,
                defaults={'longitude': longitude, 'latitude': latitude}
            )

            if not created:
                position_object.longitude = longitude
                position_object.latitude = latitude
                position_object.save()

            messages.success(request, 'Fueling station location information has been added successfully.')
            return redirect("success_okay")
    else:
        form = FuelingStationForm()

    return render(request, 'main/form.html', {'form': form})

def edit_price (request):
    pass

def dashboard(request):
    user = request.user 
    stations = Fueling_station.objects.filter(agent=user).prefetch_related('fuel_station_price')
    return render(request, 'main/dashboard.html', {'stations': stations})

def success(request):
    return render(request, 'main/success.html')
