
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
import time
from django.core.serializers import serialize
from Main.tasks import *
from rest_framework_simplejwt.views import TokenObtainPairView
from Api.helper_functions.views_functions import *
from rest_framework.permissions import IsAuthenticated
from Auth.models import UserLocation
from rest_framework import filters
from rest_framework.exceptions import NotFound
from Main.models import *
from Api.Application_api.helper_function.main_function_support import *
from rest_framework.decorators import api_view
from Api.serializers import *





'''This api returns station based on the users longitude and latitude'''
@api_view(['POST'])
def find_nearby_fueling_stations(request):
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    user = request.user

    if not latitude or not longitude:
        return Response({'error': 'Latitude and longitude must be provided.'}, status=400)

    user_position = (float(latitude), float(longitude))



    all_stations = check_if_fueling_station_is_in_cache()
    nearby_stations = process_station_fueling_by_distance (all_stations, user_position)
    serializer = FuelStationSerializer(nearby_stations, many=True)
    serialized_data = serializer.data

    fuel_stations_with_location = add_fuel_station_to_location(serialized_data, user)

    return Response(status=HTTP_200_OK, data={'fueling_stations': fuel_stations_with_location})



'''This api returns station based on the users saved local government'''
@api_view(['GET'])
def get_saved_stations (request):

    # Get user's current onboarding location
    user = request.user
    user_location = UserLocation.objects.select_related(
        'user').get(user=user)

    fueling_stations = Fueling_station.objects.filter(
        local_government=user_location.local_government)


    serializer = FuelStationSerializer(fueling_stations, many=True)
    serialized_data = serializer.data
    fuel_stations_with_location = add_fuel_station_to_location(serialized_data, user)


    return Response(status=HTTP_200_OK, data={'fueling_stations': fuel_stations_with_location})


