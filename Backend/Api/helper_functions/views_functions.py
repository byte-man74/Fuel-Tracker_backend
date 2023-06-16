import string
import random
from Main.models import Fueling_station
from django.core.cache import cache
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status

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


# Generate a random text of length 10
def check_if_vote_key_exists(data):
    return 'vote' in data


def check_vote_status(status):
    return status


def find_key_by_value(cache_object,  price_value):
    print(cache_object)

    for key, value in cache_object.items():
        if value['price'] == price_value:
            print("Key:", key)
            print("Value:", value)
            return key
            

def process_vote_request(price_value, cache_object):
    print('we are here')
    cache_key = find_key_by_value(cache_object, price_value)
    print('cahche keyy')
    print(cache_key)
    if cache_key is not None:
        print('safe')
        cache_object[cache_key]['votes'] += 1
        return Response(status=status.HTTP_200_OK)
    # todo add extra processing here for if the vote is above a certain number


def check_cache_key_for_fuel_station_id_and_process_request(data, fuel_station_id):
    station_cache_key = return_fuel_station_cache_key(fuel_station_id)

    cache_object = cache.get(station_cache_key)
    if cache_object is not None:
        price_value = data['price']  # Access price value from data dictionary

        # Check if price_value exists in cache_object keys
        if price_value is not None:
            process_vote_request(price_value, cache_object)
            return

    # Call else_function if cache_object is None or price_value not found
    else_function(station_cache_key, data)


def else_function(station_cache_key, data):
    cache_object = cache.get(station_cache_key)
    if cache_object is not None:
        num_keys = len(cache_object)

        process_cache_per_the_numbers_of_keys(
            num_keys, data, cache_object, station_cache_key)

    else:
        # create cache
        cache_instance = {
            generate_random_text(7): {
                "price": data['price'],
                "votes": 1,
                "time_initialized": datetime.now()
            }
        }
        cache.add(station_cache_key, cache_instance)
        return Response(status=status.HTTP_200_OK)


def process_cache_per_the_numbers_of_keys(num_keys, data, cache_object, station_cache_key):
    if num_keys >= 4:
        pass
    else:
        cache_object[generate_random_text(7)] = {
            "price": data['price'],
            "votes": 1,
            "time_initialized": datetime.now()
        }
        cache.set(station_cache_key, cache_object)
        return Response( status=status.HTTP_200_OK)


"""{"key":{
    "key1": {
        "price": 100,
        "votes": 2,
        "time_initialized": 120291
    },
    "key2": {
        "price": 550,
        "votes": 2,
        "time_initialized": 120291
    },
    "key3": {
        "price": 700,
        "votes": 1,
        "time_initialized": 120291
    },
    "key4": {
        "price": 100,
        "votes": 1,
        "time_initialized": 120291
    }
}}
"""
