from django.contrib.auth import get_user_model
from rest_framework import serializers
from Main.models import Fueling_station
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


#!  would check this out someother time
class FuelStationSerializer(serializers.ModelSerializer):
    model = Fueling_station
    pass
