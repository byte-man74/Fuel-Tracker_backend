from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from .serializers import UserSerializer, TokenObtainPairSerializer, FuelStationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from Main.models import Fueling_station
from Auth.models import UserLocation
from rest_framework import filters

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


'''The GetNearbyFuelingStation API view retrieves nearby fueling stations based on the user's current onboarding location and an optional search query.'''
#todo Would pass the longitude and latitude of the station
class GetNearbyFuelingStation(APIView):

    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['field1', 'field2']

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

        return Response(status=HTTP_200_OK, data={'fueling_stations': serialized_data})
    

class ViewFuelingStationInformation (APIView):
    pass
    #pass the fueling station name, deliver the image, deliver the logo