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


def check_cache_key_for_fuel_station_id_and_process_request(fuel_station_id):
        station_cache_key = return_fuel_station_cache_key(fuel_station_id)

        options = cache.get(station_cache_key)
        if options is not None:
            pass
            #try except if key exists so as to fire else function
        else:
            pass
            #else function
#check if the cache key exists.......... if it does move forward....... if it doesn't exist create one





        
'''
{"key": {
            {"price": 100}, {"votes": 2}, {"time_initialized": 120291},
            {"price": 550}, {"votes": 2}, {"time_initialized": 120291},
            {"price": 700}, {"votes": 1}, {"time_initialized": 120291},
            {"price": 100}, {"votes": 1}, {"time_initialized": 120291}
            }
}
'''