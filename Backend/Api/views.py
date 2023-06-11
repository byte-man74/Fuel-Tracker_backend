from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import UserSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
    


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer





#Get the list of all the fueling station close to 500m for the user (recent changes and updates of the prices on the top)
#get the paginated list of all the fueling station around the location. 
#search the fueling station by name and filter by state
