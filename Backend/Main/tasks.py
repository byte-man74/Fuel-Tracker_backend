from __future__ import absolute_import, unicode_literals
from Main.models import Fuel_Station_Price

from celery import shared_task


@shared_task
def update_db(object, id):
    print(object)
    price_model = Fuel_Station_Price.objects.get(station=id)
    price_model.amount = object['price']
    price_model.votes = object['votes']
    price_model.save()


@shared_task
def update_votes(id):

    fuel_station_price = Fuel_Station_Price.objects.get(
            station=id)
    # Increment the votes count
    fuel_station_price.votes += 1
    fuel_station_price.save()