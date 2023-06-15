from Main.models import Fueling_station
from django.core.cache import cache


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


def check_if_vote_key_exists(data):
    return 'value' in data


def check_vote_status(status):
    return status


def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None  # Value not found in the dictionary


def process_vote_request(price_value, cache_object):
    cache_key = find_key_by_value(cache_object, price_value)
    if cache_key is not None:
        cache_object[cache_key]['votes'] += 1



def check_cache_key_for_fuel_station_id_and_process_request(data, fuel_station_id):
    station_cache_key = return_fuel_station_cache_key(fuel_station_id)

    options = cache.get(station_cache_key)
    if options is not None:
        price_value = data['price']  # Access price value from data dictionary

        # Assuming station_cache_key has 'key' attribute
        cache_object = station_cache_key.key

        # Check if price_value exists in cache_object keys
        if price_value in cache_object.station_cache_key.keys():
            process_vote_request(price_value, cache_object)
            return
    else_function()  # Call else_function if options is None or price_value not found




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