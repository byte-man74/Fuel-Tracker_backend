
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from Auth.models import CustomUser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
import time
from django.core.serializers import serialize
from Main.tasks import update_votes, update_traffic_rating_count, update_vote_count, create_price_record
from rest_framework_simplejwt.views import TokenObtainPairView
from Api.helper_functions.views_functions import *
from rest_framework.permissions import IsAuthenticated
from Auth.models import UserLocation
from rest_framework import filters
from .serializers import *
from rest_framework.exceptions import NotFound
from Main.models import *
from django.core.cache import cache
from rest_framework.decorators import api_view
from .serializers import FuelStationCommentSerializer

'''Authentication '''






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
            position = Fuel_Station_Position.objects.select_related('station').get(station=station)
            price = Fuel_Station_Price.objects.get(station=station)
            traffic = Fuel_Station_Traffic_Rating.objects.get(station=station)
            has_voted = False


            users = price.get_voted_users()
            if request.user in users:
                has_voted = True

            # Create a dictionary with the required price fields
            price_data = {
                'amount': price.amount,
                'last_updated': price.last_updated,
                'votes': price.votes
                # Add other price fields you need
            }
            traffic_data = {
                'terrible' : traffic.terrible_rating_count,
                'average' : traffic.average_rating_count,
                'good' : traffic.good_rating_count
            }

            fuel_station_with_location = {
                'station': data,
                'position': {"longitude": position.longitude, "latitude": position.latitude},
                'price': price_data,
                'traffic' : traffic_data,
                'has_voted' : has_voted
            }

            fuel_stations_with_location.append(fuel_station_with_location)

        return Response(status=HTTP_200_OK, data={'fueling_stations': fuel_stations_with_location[:10]})

'''The ViewFuelingStationInformation is responsible for users to easily check the database and see a particular information relating to the fuel station they are interested in'''



'''station information and processing'''

@api_view(['POST'])
def find_nearby_fueling_stations(request):
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if not latitude or not longitude:
        return Response({'error': 'Latitude and longitude must be provided.'}, status=400)

    user_position = (float(latitude), float(longitude))
    has_voted = False
    nearby_stations = []

    all_stations = Fuel_Station_Position.objects.all()
    for station_position in all_stations:
        try:
            station_coords = (float(station_position.latitude), float(station_position.longitude))
        except ValueError:
            continue  # Skip invalid station coordinates

        distance = haversine(user_position[0], user_position[1], station_coords[0], station_coords[1])
        if distance <= 10.5:  # 500 meters in kilometers
            nearby_stations.append(station_position.station)

    serializer = FuelStationSerializer(nearby_stations, many=True)
    serialized_data = serializer.data

    fuel_stations_with_location = []

#there is a bottleneck here sha😭
    for data in serialized_data:
        station = Fueling_station.objects.get(id=data['id'])
        position = Fuel_Station_Position.objects.select_related('station').get(station=station)
        price = Fuel_Station_Price.objects.get(station=station)
        traffic = Fuel_Station_Traffic_Rating.objects.get(station=station)

        users = price.get_voted_users()

        if request.user in users:
            has_voted = True


        price_data = {
            'amount': price.amount,
            'last_updated': price.last_updated,
            'votes': price.votes
                # Add other price fields you need
        }
        traffic_data = {
            'terrible' : traffic.terrible_rating_count,
            'average' : traffic.average_rating_count,
            'good' : traffic.good_rating_count
        }

        fuel_station_with_location = {
            'station': data,
            'position': {"longitude": position.longitude, "latitude": position.latitude},
            'price': price_data,
            'traffic' : traffic_data,
            'has_voted' : has_voted
        }

        fuel_stations_with_location.append(fuel_station_with_location)

    return Response(status=HTTP_200_OK, data={'fueling_stations': fuel_stations_with_location})




#api to get a fueling station information
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

        users = price.get_voted_users()
        has_voted = False
        if request.user in users:
            has_voted = True


        # Create a dictionary to hold the serialized data
        serialized_data = {
            'station': FuelStationSerializer(station).data,
            'price': FuelStationPriceSerializer(price).data,
            'traffic_rating': FuelStationTrafficRatingSerializer(traffic_rating).data,
            'extra_information': FuelStationExtraInformationSerializer(extra_information).data,
            'has_voted': has_voted
        }

        return Response(serialized_data)



#api to edit price of a fueling station
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
    def get(self, request, price_id):
        try:
            price = Fuel_Station_Price.objects.get(id=price_id)
        except Fuel_Station_Price.DoesNotExist:
            return Response({'result': 'Price not found'}, status=404)

        # Check if the user has already voted for this price
        if request.user in price.get_voted_users():
            return Response({'result': 'User has already voted for this price'}, status=200)

        # Add the user to the list of voted users
        price.voted_users.add(request.user)

        # Increment the votes count (if needed)
        price.votes += 1
        price.save()

        return Response({'result': 'Vote recorded successfully'}, status=200)



'''Update traffic rating'''
class UpdateTrafficRatingCountView(APIView):
    def post(self, request, fuel_station_id):
        rating_type = request.data.get('rating_type')

        # Trigger the Celery task asynchronously
        update_traffic_rating_count(fuel_station_id, rating_type)

        return Response({'message': 'Rating count update task has been scheduled'}, status=status.HTTP_200_OK)


#api to upvote price
class UpdateVoteCountOpenCLoseView(APIView):
    def post(self, request, fuel_station_id):
        vote_type = request.data.get('vote_type')

        # Trigger the Celery task asynchronously
        update_vote_count(fuel_station_id, vote_type)

        return Response({'message': 'Vote count update task has been scheduled'}, status=status.HTTP_200_OK)

# {"vote_type": "open"}



# api to comment
@api_view(['POST'])
def create_comment(request, station_id):
    station = Fueling_station.objects.get(id=station_id)
    serializer = FuelStationCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_email=request.user.email, station=station)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#api to add state and local government to the stations
@api_view(['GET'])
def update_position(request):
    stations = Fueling_station.objects.all()
    # api_key = 'Ahndh4GZR21tp2mdoH3VYktZS7HeiGs7-UYmNhOk5gD7G7kAVuY6i57lJC8wHjrL'

    for station in stations:
        position = Fuel_Station_Position.objects.get(station=station)
        time.sleep(0.5)
        state, local_government = get_location_from_coordinates(position.latitude, position.longitude)
        print(local_government)
        station.local_government = local_government
        print("getting station")
        station.save()
    return Response(status=status.HTTP_201_CREATED)


#api to get the average price of a fueling stattion would turn it to a scheduled task later
@api_view(['GET'])
def FuelStationAveragePrice(request):
    try:
        fuel_station_prices = Fuel_Station_Price.objects.all()
        if not fuel_station_prices:
            return Response({'error': 'No prices found for this station.'}, status=status.HTTP_404_NOT_FOUND)

        total_prices = len(fuel_station_prices)
        total_amount = sum(price.amount for price in fuel_station_prices if price.amount is not None)
        if total_amount == 0:
            return Response({'avg_amount': None}, status=status.HTTP_200_OK)

        average_price = total_amount / total_prices
        return Response({'avg_amount': average_price}, status=status.HTTP_200_OK)
    except Fuel_Station_Price.DoesNotExist:
        return Response({'error': 'Fuel station not found.'}, status=status.HTTP_404_NOT_FOUND)

#get current station price
@api_view(['GET'])
def get_current_price(request, station_id):
    try:
        price = Fuel_Station_Price.objects.get(station=station_id)
        serializer = FuelStationPriceSerializer(price)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Fuel_Station_Price.DoesNotExist:
        return Response({'error': 'Price for the station not found.'}, status=status.HTTP_404_NOT_FOUND)


#api to give the user a state and a local government
@api_view(['POST'])
def create_user_location(request):
    user = request.user

    # Check if a UserLocation instance already exists for the current user
    try:
        user_location = UserLocation.objects.get(user=user)
        # If a UserLocation instance already exists, return a 200 status code
        return Response({'message': 'User location already exists.'}, status=status.HTTP_200_OK)
    except UserLocation.DoesNotExist:
        pass  # Continue with the location creation process

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


@api_view(['GET'])
def get_comments(request, station_id):
    comments = FuelStationComment.objects.filter(station=station_id).order_by('-date_time_commented')[:5]
    if not comments:
        return Response({'error': 'No comments found for the station.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = FuelStationCommentSerializer(comments, many=True)
    return Response({'comments': serializer.data}, status=status.HTTP_200_OK)



