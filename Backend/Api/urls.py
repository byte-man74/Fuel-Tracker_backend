from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from Api.Authentication.authentication import *
from Api.Analytic_tool.main import *
from Api.Authentication.first_time_process import *
from Api.Application_api.main import *
from .views import *



urlpatterns = [
    
    #authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('token/obtain/', EmailTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('change-password/', ChangePasswordView.as_view(),
         name='change_password'),
     path('edit_account/', EditAccountInfoView.as_view(), name="edit_account"),

     #application api
     path("closest_station/", find_nearby_fueling_stations, name="closest"),
     path('save_user_location', create_user_location, name="create user location"),
     path('get_nearby_fueling_stations/', get_saved_stations,
         name='get-nearby-fueling-stations'),
    path('stations_average_price/', FuelStationAveragePrice, name='fuel-station-average-price'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('view_fueling_station_info/<int:fuel_station_id>/',
         ViewFuelingStationInformation.as_view(), name='view-fueling-station-info'),
    path('edit_price/get_options/<int:fuel_station_id>/',
         EditPriceGetOptions.as_view(), name="edit-price-get-options"),
    path('add_votes/<int:fuel_station_id>/',
         VoteFuelStationPriceView.as_view(), name='add_vote'),
    path('traffic_rating/<int:fuel_station_id>/',
         UpdateTrafficRatingCountView.as_view(), name='traffic_rating'),
    path('open_or_close_status/<int:fuel_station_id>/',
         UpdateVoteCountOpenCLoseView.as_view(), name="open_or_close_status"),



     #analytic tool
     path('admin/get_all_stations/', get_all_the_stations, name="get_all_stations_admin"),
     path('admin/get_all_state_available/', get_all_station_state, name="get_all_state_available_admin"),
     path('admin/get_all_lga_available/',  get_all_station_lga, name="get_all_lga_available_admin"),
]
