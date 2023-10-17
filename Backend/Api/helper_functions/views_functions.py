import string
import random
from Main.models import Fueling_station
from datetime import datetime, timedelta
from rest_framework import status
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.response import Response
from Main.tasks import update_db, create_price_record
import requests
import requests
import logging
from django.conf import settings


'''Helper functions'''
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


def get_fuel_station_id_from_cache_key(station_cache_key):
    # Split the cache key by "_ID_" to separate the fuel station name and id
    parts = station_cache_key.split("_ID_")

    # Ensure the cache key is in the expected format
    if len(parts) == 2:
        # The fuel station id will be the second part of the split
        fuel_station_id = parts[1].split("_")[0]
        print(fuel_station_id)
        return fuel_station_id


    # Return None if the cache key is not in the expected format
    return None



def check_if_vote_key_exists(data):
    return 'vote' in data


def check_vote_status(status):
    return status


def find_key_by_value(cache_object, price_value):
    for key, value in cache_object.items():
        if value['price'] == price_value:
            return key
    return None


def find_least_engaged_object(cache_object):
    least_votes = float('inf')
    oldest_datetime = datetime.now()
    least_engaged_key = None

    for key, value in cache_object.items():
        votes = value['votes']
        datetime_initialized = value['time_initialized']

        if votes < least_votes or (votes == least_votes and datetime_initialized < oldest_datetime):
            least_votes = votes
            oldest_datetime = datetime_initialized
            least_engaged_key = key

    return least_engaged_key


def delete_least_engaged_object(cache_object):
    if cache_object is not None:
        least_engaged_key = find_least_engaged_object(cache_object)
        if least_engaged_key is not None:
            del cache_object[least_engaged_key]
            return cache_object


'''Helper functions end'''


'''Operations'''

def update_db_from_cache(cache_dictionary, station_cache_id):
    fuel_station_id = get_fuel_station_id_from_cache_key(station_cache_id)
    update_db.delay(cache_dictionary, fuel_station_id)
    create_price_record(cache_dictionary, fuel_station_id)
    cache.delete(station_cache_id)



def process_vote_request(price_value, cache_object, station_cache_key, data):
    cache_key = find_key_by_value(cache_object, price_value)
    if cache_key is not None:
        cache_object[cache_key]['votes'] += 1

        #todo fire a function here
        if cache_object[cache_key]['votes'] >= 4:
            update_db_from_cache(cache_object[cache_key], station_cache_key)
        else:
            cache.set(station_cache_key, cache_object, int(
                timedelta(hours=1.5).total_seconds()))
        return Response(status=status.HTTP_200_OK)
    else:
        else_function(station_cache_key, data)


def check_cache_key_for_fuel_station_id_and_process_request(data, fuel_station_id):
    station_cache_key = return_fuel_station_cache_key(fuel_station_id)

    cache_object = cache.get(station_cache_key)
    if cache_object is not None:
        # Access price value from data dictionary
        price_value = data.get('price')

        if price_value is not None:
            process_vote_request(price_value, cache_object,
                                 station_cache_key, data)
            return

    else:
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
        cache.set(station_cache_key, cache_instance, int(
            timedelta(hours=1.5).total_seconds()))
        return Response(status=status.HTTP_200_OK)


def process_cache_per_the_numbers_of_keys(num_keys, data, cache_object, station_cache_key):
    if num_keys >= 4:
        processed_cache_object = process_request_on_cache(data, cache_object)
        cache.set(station_cache_key, processed_cache_object,
                  int(timedelta(hours=1.5).total_seconds()))
        return Response(status=status.HTTP_200_OK)
    else:
        cache_object[generate_random_text(7)] = {
            "price": data['price'],
            "votes": 1,
            "time_initialized": datetime.now()
        }
        cache.set(station_cache_key, cache_object, int(
            timedelta(hours=1.5).total_seconds()))
        return Response(status=status.HTTP_200_OK)



def process_request_on_cache(data, cache_objects):
    cache_object = delete_least_engaged_object(cache_objects)
    cache_object[generate_random_text(7)] = {
        "price": data['price'],
        "votes": 1,
        "time_initialized": datetime.now()
    }
    return cache_object


'''Operations end'''

# Set up the logging configuration
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def extract_location_from_data(data):
    if not data.get("results"):
        return None, None

    location = data["results"][0]
    state, local_government = None, None

    for address_component in location.get("address_components", []):
        types = address_component.get("types", [])
        if "administrative_area_level_1" in types:
            state = address_component["long_name"]
        if "locality" in types or "administrative_area_level_2" in types:
            local_government = address_component["long_name"]

    return state, local_government



def get_location_from_coordinates(latitude, longitude):
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    
    if not GOOGLE_API_KEY:
        logger.error("No Google API key found.")
        return None, None

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": GOOGLE_API_KEY,
        "result_type": "political",
        "language": "en",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        state, local_government = extract_location_from_data(response.json())
        if state and local_government:
            return state, local_government
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")

    return None, None



