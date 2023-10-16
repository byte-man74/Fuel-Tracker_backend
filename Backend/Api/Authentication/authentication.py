
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from Api.serializers import *
from Auth.models import CustomUser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
import time
from django.core.serializers import serialize
from rest_framework_simplejwt.views import TokenObtainPairView
from Api.helper_functions.views_functions import *
from rest_framework.permissions import IsAuthenticated
from Auth.models import UserLocation
from rest_framework import filters
from rest_framework.exceptions import NotFound
from Main.models import *
from django.core.cache import cache
from rest_framework.decorators import api_view




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



'''Api to get email address'''
@api_view(['GET'])
def GetEmailAddress (request):
    user = request.user
    email = user.email

    data = {'email' : email}
    return Response (data, status= status.HTTP_200_OK)




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

