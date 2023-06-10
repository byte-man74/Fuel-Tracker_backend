from django.db import models

# Create your models here.
class Fueling_station(models.Model):
    name = models.CharField( max_length=50)
    logo = models.ImageField( upload_to="Fueling_station_Image_directory")
    background_image = models.ImageField( upload_to="Fueling_station_Image_directory")
    #! Add Price here (foreign key) 
    #! Add Traffic_rating here (foreign key)
    #! Add Position here (foreign key)
    #! Add Extra_info here (foreign key)

    #todo Create a signal to create the fields for all the extra's here

    def __str__(self):
        return self.name
    

class Fuel_Station_Price (models.Model):
    amount = models.BigIntegerField(null=True)
    votes = models.IntegerField(default=0)
    last_updated = models.DateTimeField( auto_now=False, auto_now_add=False) #! find out the model that changes this field on edit of the model class


    def get_formatted_amount(self):
       formatted_amount=  "{:,}".format(self.amount)
       return formatted_amount
    
    #!find a way of grabbing the fuel station and representing it in a name here
    def __str__(self):
        return self.name
    
class Fuel_Station_Traffic_Rating (models.Model):
    terrible_rating_count = models.IntegerField(default=0)
    average_rating_count = models.IntegerField(default=0)
    good_rating_count = models.IntegerField(default=0)

    #!find a way of grabbing the fuel station and representing it in a name here
    def __str__(self):
        return self.name
    
    # todo find a way of returning the percentages of the number of votes

class Fuel_Station_Position (models.Model):
    longitude = models.CharField(max_length=200, null=True)
    latitude = models.CharField(max_length=200, null=True)

    #!find a way of grabbing the fuel station and representing it in a name here
    def __str__(self):
        return self.name


class Fuel_Station_Extra_Information (models.Model):
    number_of_votes_for_fuel_station_being_open  = models.IntegerField(default=0)
    number_of_votes_for_fuel_station_being_close = models.IntegerField(default=0)

    #!find a way of grabbing the fuel station and representing it in a name here
    def __str__(self):
        return self.name
    
    
