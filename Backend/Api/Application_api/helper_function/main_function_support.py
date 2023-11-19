from django.core.cache import cache
from Main.models import *
import math
# Constants
DAY_DURATION = 24 * 60 * 60
CACHE_KEY = 'all_fueling_station'

def check_if_fueling_station_is_in_cache ():
    cache_object = cache.get("all_fueling_station") 

    if cache_object is None:
        stations = cache_and_return_fueling_stations()
        return stations
    
    return cache_object


def check_distance_exist_in_cache ():
    cache_object = cache.get("all_station_distance")

    if cache_object is None:
        location_instance = cache_and_return_fueling_station_distance()
        return location_instance
    return cache_object



def cache_and_return_fueling_station_distance():
    DAY_DURATION = 24 * 60 * 60
    fueling_station_distance = Fuel_Station_Position.objects.all()
    cache.set('all_station_distance', fueling_station_distance, DAY_DURATION)

    return fueling_station_distance



def cache_and_return_fueling_stations():
    DAY_DURATION = 24 * 60 * 60
    fueling_station = Fueling_station.objects.all()
    cache.set('all_fueling_station', fueling_station, DAY_DURATION)

    return fueling_station


def process_station_fueling_by_distance (all_stations, user_position):
    nearby_stations = []

    for station_position in all_stations:
        try:
            station_coords = (float(station_position.latitude), float(station_position.longitude))
        except ValueError:
            continue  # Skip invalid station coordinates

        distance = haversine(user_position[0], user_position[1], station_coords[0], station_coords[1])
        if distance <= 10.5:  # 500 meters in kilometers
            nearby_stations.append(station_position.station)

    return nearby_stations




def check_if_state_cache_exist ():
    state_available = cache.get("state_available")
    if state_available is None:
        states = cache_and_return_state()
        return states
    return state_available


def cache_and_return_state():
    DAY_DURATION = 24 * 60 * 60
    all_stations = check_if_fueling_station_is_in_cache()

    # Check if all_stations is iterable, if not return an error response or handle it appropriately
    if all_stations is None:
        return None

    state_set = set()  # Using a set for better performance in membership checks
    for station in all_stations:
        state_set.add(station.state)

    cache.set('all_fueling_station', list(state_set), DAY_DURATION)
    return list(state_set)





'''local government'''
def get_cached_local_governments():
    """
    Check if cached local governments exist. If not, cache and return them.
    """
    lga_available = cache.get("all_lga")

    if lga_available is None:
        lga_available = cache_and_return_lga()

    return lga_available

def cache_and_return_lga():
    """
    Cache the list of unique local governments from fueling stations and return it.
    """
    all_stations = check_if_fueling_station_is_in_cache()
    # Check if all_stations is iterable, if not, return None.
    if all_stations is None:
        return None

    lga_set = {station.local_government for station in all_stations}  # Using set comprehension

    cache.set("all_lga", list(lga_set), DAY_DURATION)
    return list(lga_set)


def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    earth_radius_km = 6371.0
    distance_km = earth_radius_km * c

    return distance_km




def add_fuel_station_to_location(serialized_data, user=None):
    fuel_stations_with_location = []
    has_voted = False


    for data in serialized_data:
        station = Fueling_station.objects.get(id=data['id'])


        #redis cache here too
        position = Fuel_Station_Position.objects.select_related('station').get(station=station.id)
        price = Fuel_Station_Price.objects.get(station=station.id)
        traffic = Fuel_Station_Traffic_Rating.objects.get(station=station.id)

        users = price.get_voted_users()

        if user in users and user is not None:
            has_voted = True


        price_data = {
            'amount': price.amount,
            'last_updated': price.last_updated,
            'votes': price.votes
                # Add other price fields you need
        }
        traffic_data = {
            'terrible' : traffic.terrible_rating_count,
            'average' : traffic.average_rating_count,
            'good' : traffic.good_rating_count
        }

        fuel_station_with_location = {
            'station': data,
            'position': {"longitude": position.longitude, "latitude": position.latitude},
            'price': price_data,
            'traffic' : traffic_data,
            'has_voted' : has_voted
        }

        fuel_stations_with_location.append(fuel_station_with_location)

    return fuel_stations_with_location
