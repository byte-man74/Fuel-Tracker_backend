
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from Auth.models import CustomUser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import time
from Main.tasks import update_votes, update_traffic_rating_count, update_vote_count, create_price_record
from rest_framework_simplejwt.views import TokenObtainPairView
from Api.helper_functions.views_functions import (return_fuel_station_cache_key,
                                                  check_if_vote_key_exists,
                                                  check_vote_status,
                                                  check_cache_key_for_fuel_station_id_and_process_request,
                                                  else_function, get_location_info, get_location_from_coordinates)
from rest_framework.permissions import IsAuthenticated
from Auth.models import UserLocation
from rest_framework import filters
from .serializers import (UserSerializer,
                          TokenObtainPairSerializer,
                          FuelStationSerializer,
                          FuelStationPriceSerializer,
                          FuelStationTrafficRatingSerializer,
                          FuelStationExtraInformationSerializer,
                          FuelStationPositionSerializer,
                          UserLocationSerializer)
from rest_framework.exceptions import NotFound
from Main.models import (Fueling_station,
                         Fuel_Station_Price,
                         Fuel_Station_Traffic_Rating,
                         Fuel_Station_Position,
                         Fuel_Station_Extra_Information)
from django.core.cache import cache
from rest_framework.decorators import api_view
from .serializers import FuelStationCommentSerializer

'''The RegisterView is responsible for user creation account and onboarding of user '''


class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            self.create_user(serializer.validated_data)
            return Response(status=HTTP_201_CREATED)

        return self.invalid_user_response(serializer.errors)

    def create_user(self, validated_data):
        get_user_model().objects.create_user(**validated_data)

    def invalid_user_response(self, errors):
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': errors})


'''This is responsible for the login functionality of the api'''


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


'''change passsword'''


class ChangePasswordView(APIView):
    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        # Verify the user's current password
        if not user.check_password(current_password):
            return Response({'error': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password using make_password function
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


'''Edit account info'''


class EditAccountInfoView(APIView):
    def put(self, request):
        user = request.user
        email = request.data.get('email')
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        # Check if email is provided and not already taken by another user
        if email:
            if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
                return Response({'error': 'Email is already in use'}, status=status.HTTP_400_BAD_REQUEST)
            user.email = email


        # Update the first name and last name
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()

        return Response({'message': 'Account information updated successfully'}, status=status.HTTP_200_OK)


'''The GetNearbyFuelingStation API view retrieves nearby fueling stations based on the user's current onboarding location and an optional search query.'''
# todo Would pass the longitude and latitude of the station


class GetNearbyFuelingStation(APIView):

    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    def get(self, request, *args, **kwargs):
        serializer = FuelStationSerializer()
        search_query = request.query_params.get('search')

        # Get user's current onboarding location
        user = request.user
        user_location = UserLocation.objects.select_related(
            'user').get(user=user)

        fueling_stations = Fueling_station.objects.filter(
            local_government=user_location.local_government)

        # Filter fueling stations within the range of the user's location
        if search_query:
            fueling_stations = fueling_stations.filter(
                name__icontains=search_query)

        serializer = FuelStationSerializer(fueling_stations, many=True)
        serialized_data = serializer.data

        fuel_stations_with_location = []

        for data in serialized_data:
            station = Fueling_station.objects.get(id=data['id'])
            position = Fuel_Station_Position.objects.select_related(
                'station').get(station=station)
            print(position.longitude)
            fuel_station_with_location = {
                'station': data, 'position': {"longitude": position.longitude, "latitude": position.latitude}}
            fuel_stations_with_location.append(fuel_station_with_location)

        return Response(status=HTTP_200_OK, data={'fueling_stations': fuel_station_with_location})


'''The ViewFuelingStationInformation is responsible for users to easily check the database and see a particular information relating to the fuel station they are interested in'''


class ViewFuelingStationInformation (APIView):
    # todo ......add a cache checker herre for performance
    def get(self, request, fuel_station_id):
        try:
            station = Fueling_station.objects.get(id=fuel_station_id)
        except Fueling_station.DoesNotExist:
            raise NotFound("Fueling station does not exist.")

        price = Fuel_Station_Price.objects.select_related(
            'station').get(station=station)
        traffic_rating = Fuel_Station_Traffic_Rating.objects.select_related(
            'station').get(station=station)
        extra_information = Fuel_Station_Extra_Information.objects.select_related(
            'station').get(station=station)

        # Create a dictionary to hold the serialized data
        serialized_data = {
            'station': FuelStationSerializer(station).data,
            'price': FuelStationPriceSerializer(price).data,
            'traffic_rating': FuelStationTrafficRatingSerializer(traffic_rating).data,
            'extra_information': FuelStationExtraInformationSerializer(extra_information).data,
        }

        return Response(serialized_data)




class EditPriceGetOptions(APIView):
    def get(self, request, fuel_station_id):
        station_cache_key = return_fuel_station_cache_key(fuel_station_id)
        cache_object = cache.get(station_cache_key)

        if cache_object is not None:
            return Response(data={'cache_object': cache_object}, status=status.HTTP_200_OK)
        else:
            return Response(data={'details': 'no options'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, fuel_station_id):
        station_cache_key = return_fuel_station_cache_key(fuel_station_id)
        data = request.data
        vote_validation = check_if_vote_key_exists(data)

        if not vote_validation:
            raise ValueError("Vote key 'value' does not exist in the data.")

        vote_status = check_vote_status(data)

        if vote_status:
            check_cache_key_for_fuel_station_id_and_process_request(
                data, fuel_station_id)
            return Response(status=status.HTTP_200_OK)
        else:
            response = else_function(station_cache_key, data)
            if response is not None:
                return response
            else:
                return Response(status=status.HTTP_200_OK)

            # {'vote": true, 'price': 300}

'''vote for a fuel price'''
class VoteFuelStationPriceView(APIView):
    def post(self, request, fuel_station_id):
        update_votes.delay(fuel_station_id)
        return Response({'message': 'Vote added successfully'}, status=status.HTTP_200_OK)


'''Update traffic rating'''
class UpdateTrafficRatingCountView(APIView):
    def post(self, request, fuel_station_id):
        rating_type = request.data.get('rating_type')

        # Trigger the Celery task asynchronously
        update_traffic_rating_count.delay(fuel_station_id, rating_type)

        return Response({'message': 'Rating count update task has been scheduled'}, status=status.HTTP_200_OK)


class UpdateVoteCountOpenCLoseView(APIView):
    def post(self, request, fuel_station_id):
        vote_type = request.data.get('vote_type')

        # Trigger the Celery task asynchronously
        update_vote_count.delay(fuel_station_id, vote_type)

        return Response({'message': 'Vote count update task has been scheduled'}, status=status.HTTP_200_OK)

# {"vote_type": "open"}



# todo

# Assuming you have Django and Django Rest Framework installed and configured

@api_view(['POST'])
def create_comment(request):
    serializer = FuelStationCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def update_position(request):
    stations = Fueling_station.objects.all()
    api_key = 'Ahndh4GZR21tp2mdoH3VYktZS7HeiGs7-UYmNhOk5gD7G7kAVuY6i57lJC8wHjrL'

    for station in stations:
        position = Fuel_Station_Position.objects.get(station=station)
        time.sleep(0.5)
        state, local_government = get_location_from_coordinates(position.latitude, position.longitude)
        print(local_government)
        station.local_government = local_government
        print("getting station")
        station.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_user_location(request):
    user = request.user

    # Extract state and local government based on the latitude and longitude
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    state, local_government = get_location_from_coordinates(latitude, longitude)

    if state and local_government:
        location_data = {
            'state': state,
            'local_government': local_government,
            'user': user.id
        }
        serializer = UserLocationSerializer(data=location_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Location data not found.'}, status=status.HTTP_404_NOT_FOUND)