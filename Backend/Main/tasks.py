from __future__ import absolute_import, unicode_literals
from .models import Fuel_Station_Extra_Information
from .models import Fuel_Station_Traffic_Rating
from Main.models import Fuel_Station_Price
from Records.models import Price_Change_Record

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


@shared_task
def update_vote_count(station_id, vote_type):
    try:
        fuel_station_info = Fuel_Station_Extra_Information.objects.get(
            station_id=station_id)
    except Fuel_Station_Extra_Information.DoesNotExist:
        # Handle error if the fuel station extra information object doesn't exist
        return

    # Update the vote count based on the vote_type
    if vote_type == 'open':
        fuel_station_info.number_of_votes_for_fuel_station_being_open += 1
    elif vote_type == 'close':
        fuel_station_info.number_of_votes_for_fuel_station_being_close += 1

    fuel_station_info.save()


@shared_task
def create_price_record(fuel_station_id, updated_price):
    try:
        station_price = Fuel_Station_Price.objects.get(station=fuel_station_id)
    except Fuel_Station_Price.DoesNotExist:
        return

    price_object = Price_Change_Record.objects.create(
        station=fuel_station_id,
        initial_price=station_price.amount,
        new_price=updated_price
    )
    price_object.save()
