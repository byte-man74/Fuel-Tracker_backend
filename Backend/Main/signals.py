from django.db.models.signals import post_save
from .models import Fueling_station, Fuel_Station_Extra_Information, Fuel_Station_Position, Fuel_Station_Price, Fuel_Station_Traffic_Rating
from django.dispatch import receiver


@receiver(post_save, sender=Fueling_station)
def save_fuel_station_related_information(sender, instance, created, **kwargs):
    if created:
        Fuel_Station_Extra_Information.objects.get_or_create(
            station=instance)
        Fuel_Station_Position.objects.get_or_create(
            station=instance)
        Fuel_Station_Price.objects.get_or_create(
            station=instance)
        Fuel_Station_Traffic_Rating.objects.get_or_create(
            station=instance)
