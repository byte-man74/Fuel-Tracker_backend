from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (EmailTokenObtainPairView, RegisterView, GetNearbyFuelingStation,
                    ViewFuelingStationInformation, EditPriceGetOptions, ChangePasswordView, 
                    EditAccountInfoView, VoteFuelStationPriceView, UpdateTrafficRatingCountView,
                    UpdateVoteCountOpenCLoseView, create_user_location)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/obtain/', EmailTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('change-password/', ChangePasswordView.as_view(),
         name='change_password'),
     path('save_user_location', create_user_location, name="create user location"),
    path('edit_account/', EditAccountInfoView.as_view(), name="edit_account"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_nearby_fueling_stations/', GetNearbyFuelingStation.as_view(),
         name='get-nearby-fueling-stations'),
    path('view_fueling_station_info/<int:fuel_station_id>/',
         ViewFuelingStationInformation.as_view(), name='view-fueling-station-info'),
    path('edit_price/get_options/<int:fuel_station_id>/',
         EditPriceGetOptions.as_view(), name="edit-price-get-options"),
    path('add_votes/<int:fuel_station_id>/',
         VoteFuelStationPriceView.as_view(), name='add_vote'),
    path('traffic_rating/<int:fuel_station_id>/',
         UpdateTrafficRatingCountView.as_view(), name='traffic_rating'),
    path('open_or_close_status/<int:fuel_station_id>/',
         UpdateVoteCountOpenCLoseView.as_view(), name="open_or_close_status")
]
