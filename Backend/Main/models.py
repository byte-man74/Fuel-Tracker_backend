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


