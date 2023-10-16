from Auth.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Api.helper_functions.views_functions import *
from Api.serializers import *



@api_view(['POST'])
def create_user_location(request):
    user = request.user

    # Check if a UserLocation instance already exists for the current user
    existing_location = UserLocation.objects.filter(user=user).first()
    if existing_location:
        return Response({'message': 'User location already exists.'}, status=status.HTTP_200_OK)

    # Ensure latitude and longitude are provided in the request data
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    if not latitude or not longitude:
        return Response({'message': 'Latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Extract state and local government based on the coordinates
    try:
        state, local_government = get_location_from_coordinates(latitude, longitude)
    except Exception as e:  # Handle specific exceptions that could arise from the function if any
        return Response({'message': f"Error determining location: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not state or not local_government:
        return Response({'message': 'Location data not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize and save the UserLocation data
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