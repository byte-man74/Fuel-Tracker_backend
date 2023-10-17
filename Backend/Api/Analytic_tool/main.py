from Api.Application_api.helper_function.main_function_support import *


def get_all_the_station (request):
    all_stations = check_if_fueling_station_is_in_cache()
