from django.urls import path
from .views import create_fueling_station, fuel_station_position, success, landing_page, login_page, sign_up

urlpatterns = [
    path('', landing_page, name="Home"),
    path ('sign_up', sign_up, name="sign_up"),
    path('login', login_page, name="login"),
    path('create_station', create_fueling_station, name="Add Fueling Station"),
    path('location/<int:fueling_station_id>', fuel_station_position , name="Fuel station position"),
    path('success', success, name="success_okay")
]
