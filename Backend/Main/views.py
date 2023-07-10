from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .forms import FuelingStationForm, LoginForm, SignupForm, FuelStationPriceForm
from .models import Fueling_station, Fuel_Station_Position, Fuel_Station_Price
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
            fueling_station.agent = request.user
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

            return redirect("edit_price", station.id)
    else:
        form = FuelingStationForm()

    return render(request, 'main/form.html', {'form': form})

def edit_fuel_station_price(request, station_id):
    fueling_station = Fueling_station.objects.get(id=station_id)
    try:
        fuel_station_price = Fuel_Station_Price.objects.get(station=fueling_station)
    except Fuel_Station_Price.DoesNotExist:
        fuel_station_price = Fuel_Station_Price(station=fueling_station)

    if request.method == 'POST':
        form = FuelStationPriceForm(request.POST, instance=fuel_station_price)
        if form.is_valid():
            form.save()
            return redirect('success_okay')  # Replace 'dashboard' with the desired URL for the dashboard view
    else:
        form = FuelStationPriceForm(instance=fuel_station_price)

    return render(request, 'main/form.html', {'form': form, 'station_id': station_id})

def dashboard(request):
    user = request.user 
    stations = Fueling_station.objects.filter(agent=user).prefetch_related('fuel_station_price')
    return render(request, 'main/dashboard.html', {'stations': stations})

def success(request):
    return render(request, 'main/success.html')
