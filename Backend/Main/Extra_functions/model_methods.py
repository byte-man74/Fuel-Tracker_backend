from Main.models import Fueling_station

def get_fuel_station_instance(self):
    id = self.station
    try:
        return Fueling_station.objects.get(id=id)
    except:
        pass