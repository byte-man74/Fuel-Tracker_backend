from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import EmailTokenObtainPairView, RegisterView, GetNearbyFuelingStation, ViewFuelingStationInformation, EditPriceGetOptions

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/obtain/', EmailTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_nearby_fueling_stations/', GetNearbyFuelingStation.as_view(),
         name='get-nearby-fueling-stations'),
    path('view_fueling_station_info/<int:fuel_station_id>/',
         ViewFuelingStationInformation.as_view(), name='view-fueling-station-info'),
    path('edit_price/get_options/<int:fuel_station_id>/',
         EditPriceGetOptions.as_view(), name="edit-price-get-options"),
]
