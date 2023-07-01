from django.urls import path
from .views import create_fueling_station

urlpatterns = [
    path('', create_fueling_station, name="Add Fueling Station")
]
