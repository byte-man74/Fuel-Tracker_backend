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

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)

        #? Here this is just saving the user's information if its valid
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        
        #? Firing a function for when the user's information is invalid
        else:
            return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
    


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer



#todo 'Add pagination to this end point'
#todo 'Add search functionalty to this end point'
class GetNearbyFuelingStation (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        serializer = FuelStationSerializer
        #? Mock
        '''serializer = bar_graph_serializer(instance=data, many=True)'''

        #? Get user's current onboarding location
        user = self.request.user()
        user_location = UserLocation.objects.select_related('user').get(user=user)

        Fueling_station.objects.filter(
            local_goverment=user_location.local_goverment)

        return Response(status=HTTP_200_OK, data={'fueling_station': serializer.errors})




#Get the list of all the fueling station close to 500m for the user (recent changes and updates of the prices on the top)
#get the paginated list of all the fueling station around the location. 
#search the fueling station by name and filter by state
