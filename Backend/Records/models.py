from django.db import models

# Create your models here.
class Price_Change_Record (models.Model):
    station = models.ForeignKey("Main.Fueling_station", on_delete=models.CASCADE)
    inital_price = models.BigIntegerField()
    new_price = models.BigIntegerField()
    date_time_modified = models.DateTimeField( auto_now=True)


    def __str__(self):
        return (f"{self.station.name} price change")
    