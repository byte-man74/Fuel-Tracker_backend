from django.contrib.auth import get_user_model
from rest_framework import serializers
from Main.models import Fueling_station, Fuel_Station_Position, Fuel_Station_Price, Fuel_Station_Traffic_Rating, Fuel_Station_Extra_Information
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from Main.models import FuelStationComment
from django.utils import timezone
from Auth.models import UserLocation


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


#!  would check this out someother time
class FuelStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fueling_station
        fields = '__all__'


class FuelStationPriceSerializer (serializers.ModelSerializer):
    class Meta:
        model = Fuel_Station_Price
        fields = ('amount', 'votes', 'last_updated')


class FuelStationTrafficRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel_Station_Traffic_Rating
        fields = ('terrible_rating_count',
                  'average_rating_count', 'good_rating_count')


class FuelStationExtraInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel_Station_Extra_Information
        fields = ('number_of_votes_for_fuel_station_being_open',
                  'number_of_votes_for_fuel_station_being_close')


class FuelStationPositionSerializer (serializers.Serializer):
    class Meta:
        model = Fuel_Station_Position
        fields = ('longitude', 'latitude')


class FuelStationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelStationComment
        fields = ('station', 'user_email', 'date_time_commented')
        read_only_fields = ('date_time_commented',)

    def create(self, validated_data):
        validated_data['date_time_commented'] = timezone.now()
        return super().create(validated_data)
    
class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = '__all__'