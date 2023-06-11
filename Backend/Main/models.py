from django.db import models


# Create your models here.


class Fueling_station(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(
        upload_to="Fueling_station_Image_directory", null=True)
    background_image = models.ImageField(
        upload_to="Fueling_station_Image_directory", null=True)
    local_goverment = models.CharField( max_length=50)

    def __str__(self):
        return self.name


class Fuel_Station_Price (models.Model):
    amount = models.BigIntegerField(null=True, default=0)
    votes = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    station = models.OneToOneField(
        "Main.Fueling_station", on_delete=models.CASCADE)

    def get_formatted_amount(self):
        formatted_amount = "{:,}".format(self.amount)
        formatted_amount_with_symbol = f'₦{formatted_amount}'
        return formatted_amount_with_symbol

    def __str__(self):
        Fuel_station_instance = self.station
        Fuel_station_name = Fuel_station_instance.name
        
        return f"{Fuel_station_name} price object"


class Fuel_Station_Traffic_Rating (models.Model):
    terrible_rating_count = models.IntegerField(default=0)
    average_rating_count = models.IntegerField(default=0)
    good_rating_count = models.IntegerField(default=0)
    station = models.OneToOneField(
        "Main.Fueling_station", on_delete=models.CASCADE)

    def __str__(self):
        Fuel_station_instance = self.station
        Fuel_station_name = Fuel_station_instance.name

        return f"{Fuel_station_name} traffic object"

class Fuel_Station_Position (models.Model):
    longitude = models.CharField(max_length=200, null=True)
    latitude = models.CharField(max_length=200, null=True)
    station = models.OneToOneField(
        "Main.Fueling_station", on_delete=models.CASCADE)

    def __str__(self):
        Fuel_station_instance = self.station
        Fuel_station_name = Fuel_station_instance.name

        return f"{Fuel_station_name} position object"

class Fuel_Station_Extra_Information (models.Model):
    number_of_votes_for_fuel_station_being_open = models.IntegerField(
        default=0)
    number_of_votes_for_fuel_station_being_close = models.IntegerField(
        default=0)
    station = models.OneToOneField(
        "Main.Fueling_station", on_delete=models.CASCADE)


    def __str__(self):
        Fuel_station_instance = self.station
        Fuel_station_name = Fuel_station_instance.name

        return f"{Fuel_station_name} extra informtion object"
