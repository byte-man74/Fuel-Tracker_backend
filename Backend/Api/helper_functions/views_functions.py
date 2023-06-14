from Main.models import Fueling_station

def return_fuel_station_cache_key(id):
    station = Fueling_station.objects.get(id)
    return f"{station.name} with ID of {id} cache key"
