from __future__ import absolute_import, unicode_literals
from .models import Fuel_Station_Traffic_Rating
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


@shared_task
def update_traffic_rating_count(fuel_station_id, rating_type):
    try:
        fuel_station_traffic = Fuel_Station_Traffic_Rating.objects.get(
            station_id=fuel_station_id)
    except Fuel_Station_Traffic_Rating.DoesNotExist:
        # Handle error if the fuel station traffic object doesn't exist
        return

    # Update the rating count based on the rating_type
    if rating_type == 'terrible':
        fuel_station_traffic.terrible_rating_count += 1
    elif rating_type == 'average':
        fuel_station_traffic.average_rating_count += 1
    elif rating_type == 'good':
        fuel_station_traffic.good_rating_count += 1

    fuel_station_traffic.save()
