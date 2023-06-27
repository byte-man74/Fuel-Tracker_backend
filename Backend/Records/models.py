from django.db import models

# Create your models here.
class Fuel_Change_Record(models.Model):
    station = models.OneToOneField( "Main.Fueling_station", on_delete=models.CASCADE)
    price = models.BigIntegerField()
    date = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.station