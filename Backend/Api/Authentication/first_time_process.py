from Auth.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Api.helper_functions.views_functions import *
from Api.serializers import *



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