from django.db import models
from django.utils import timezone

# Create your models here.


class Fueling_station(models.Model):
    name = models.CharField(max_length=50, help_text="name of fueling station", verbose_name='Fueling Station Name')
    logo_url = models.CharField( max_length=200, null=True)
    background_image_url = models.CharField( max_length=200, null=True)
    local_government = models.CharField( max_length=50)
    address = models.CharField(null=True,  max_length=50)
    contact_information = models.CharField(null=True,  max_length=50, help_text="Please provide a valid phone number of the fuel station attendant")

    agent = models.ForeignKey("Auth.CustomUser",  on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Fuel_Station_Price (models.Model):
    amount = models.BigIntegerField(null=True, default=0)
    votes = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=False)
    station = models.OneToOneField(
        "Main.Fueling_station", on_delete=models.CASCADE)
    voted_users = models.ManyToManyField("Auth.CustomUser")


    def get_formatted_amount(self):
        formatted_amount = "{:,}".format(self.amount)
        formatted_amount_with_symbol = f'₦{formatted_amount}'
        return formatted_amount_with_symbol

    def __str__(self):
        Fuel_station_instance = self.station
        Fuel_station_name = Fuel_station_instance.name

        return f"{Fuel_station_name} price object"

    def get_voted_users(self):
        return self.voted_users.all()

    def save(self, *args, **kwargs):
        if self.pk is None:
            # This is a new instance being created
            self.last_updated = timezone.now()
        else:
            # This is an existing instance being updated
            original = Fuel_Station_Price.objects.get(pk=self.pk)
            if self.amount != original.amount:
                self.last_updated = timezone.now()

        super().save(*args, **kwargs)



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

class FuelStationComment(models.Model):
    station = models.ForeignKey("Main.Fueling_station", on_delete=models.CASCADE, blank=True)
    user_email = models.CharField(max_length=50, blank=True)
    date_time_commented = models.DateTimeField(auto_now=True, auto_now_add=False)
    comment = models.TextField(null=True)

    @classmethod
    def get_recent_comments(cls):
        return cls.objects.order_by('-date_time_commented')[:5]

    def __str__(self):
        return f"{self.user_email} comment"


class Images_on_station (models.Model):
    station_name = models.CharField(max_length=50)
    station_logo = models.ImageField(upload_to="logo")
    station_background = models.ImageField(upload_to="background")

    def __str__(self):
        return self.station_name + "image object"
