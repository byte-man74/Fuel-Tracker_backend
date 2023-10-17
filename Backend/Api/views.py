
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










            # {'vote": true, 'price': 300}

