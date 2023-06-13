
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import EmailTokenObtainPairView, RegisterView, GetNearbyFuelingStation, ViewFuelingStationInformation

urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('token/obtain/', EmailTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_nearby_feuling_stations', GetNearbyFuelingStation.as_view(),
         name='get_nearby_feuling_stations'),
    path('view_fueling_station_info/<str:fuel_station_id>',
         ViewFuelingStationInformation.as_view(), name='view_fueling_station_info')
]
