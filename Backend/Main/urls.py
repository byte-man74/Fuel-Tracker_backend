from django.urls import path
from .views import add_fueling_station

urlpatterns = [
    path('', add_fueling_station, name="Add Fueling Station")
]
