import string
import random
from Main.models import Fueling_station
from datetime import datetime
from rest_framework import status
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.response import Response


@staticmethod
def return_fuel_station_cache_key(id):
    try:
        station = Fueling_station.objects.only('name').get(id=id)
        # Generate a cache-safe key by removing invalid characters
        safe_name = "".join(c for c in station.name if c.isalnum())
        return f"{safe_name}_ID_{id}_cache_key"
    except Fueling_station.DoesNotExist:
        # Handle the case when the fuel station with the given ID doesn't exist
        raise ValueError("Fuel station does not exist")


def generate_random_text(length):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation + " "

    # Generate random text by randomly selecting characters from the defined set
    random_text = ''.join(random.choice(characters) for _ in range(length))
    return random_text


def check_if_vote_key_exists(data):
    return 'vote' in data


def check_vote_status(status):
    return status


def find_key_by_value(cache_object, price_value):
    for key, value in cache_object.items():
        if value['price'] == price_value:
            print('yes key exists!')
            return key
    return None


def process_vote_request(price_value, cache_object, station_cache_key):
    cache_key = find_key_by_value(cache_object, price_value)
    if cache_key is not None:
        cache_object[cache_key]['votes'] += 1
        cache.set(station_cache_key, cache_object)
        return Response(status=status.HTTP_200_OK)
    # Add extra processing here for when the vote is above a certain number


def check_cache_key_for_fuel_station_id_and_process_request(data, fuel_station_id):
    station_cache_key = return_fuel_station_cache_key(fuel_station_id)

    cache_object = cache.get(station_cache_key)
    if cache_object is not None:
        # Access price value from data dictionary
        price_value = data.get('price')

        if price_value is not None:
            process_vote_request(price_value, cache_object, station_cache_key)
            return

    else_function(station_cache_key, data)


def else_function(station_cache_key, data):
    cache_object = cache.get(station_cache_key)
    if cache_object is not None:
        num_keys = len(cache_object)

        return process_cache_per_the_numbers_of_keys(
            num_keys, data, cache_object, station_cache_key)

    else:
        # Create cache
        cache_instance = {
            generate_random_text(7): {
                "price": data['price'],
                "votes": 1,
                "time_initialized": datetime.now()
            }
        }
        cache.set(station_cache_key, cache_instance)
        return Response(status=status.HTTP_200_OK)


def process_cache_per_the_numbers_of_keys(num_keys, data, cache_object, station_cache_key):
    if num_keys >= 4:
        return Response(status=status.HTTP_200_OK)
    else:
        cache_object[generate_random_text(7)] = {
            "price": data['price'],
            "votes": 1,
            "time_initialized": datetime.now()
        }
        cache.set(station_cache_key, cache_object)
        return Response(status=status.HTTP_200_OK)

# Your remaining code...
