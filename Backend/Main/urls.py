from django.urls import path
from .views import create_fueling_station, fuel_station_position, success

urlpatterns = [
    path('', create_fueling_station, name="Add Fueling Station"),
    path('location/<int:fueling_station_id>', fuel_station_position , name="Fuel station position"),
    path('success', success, name="success")

]
