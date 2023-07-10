from django.urls import path
from .views import create_fueling_station, success, dashboard, landing_page, login_page, sign_up, edit_fuel_station_price

urlpatterns = [
    path('', landing_page, name="Home"),
    path ('sign_up', sign_up, name="sign_up"),
    path('login', login_page, name="login"),
    path('create_station', create_fueling_station, name="Add Fueling Station"),
    path ('edit_price/<str:station_id>', edit_fuel_station_price, name="edit_price"),
    path ('dashboard', dashboard, name="dashboard"),
    path('success', success, name="success_okay")
]
