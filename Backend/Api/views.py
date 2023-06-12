from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from .serializers import UserSerializer, TokenObtainPairSerializer, FuelStationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from Main.models import Fueling_station
from Auth.models import UserLocation


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
    
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

#todo 'Add pagination to this end point'
#todo 'Add search functionalty to this end point'
class GetNearbyFuelingStation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = FuelStationSerializer()

        # Get user's current onboarding location
        user = request.user
        user_location = UserLocation.objects.select_related(
            'user').get(user=user)

        fueling_stations = Fueling_station.objects.filter(
            local_government=user_location.local_government)

        serialized_stations = serializer(fueling_stations, many=True).data

        return Response(status=HTTP_200_OK, data={'fueling_stations': serialized_stations})




#Get the list of all the fueling station close to 500m for the user (recent changes and updates of the prices on the top)
#get the paginated list of all the fueling station around the location. 
#search the fueling station by name and filter by state
