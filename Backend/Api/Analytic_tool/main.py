from Api.Application_api.helper_function.main_function_support import *
from Api.serializers import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_all_the_stations (request):
    all_stations = check_if_fueling_station_is_in_cache()
    serializer = FuelStationSerializer(all_stations, many=True)
    serialized_data = serializer.data
    print("data processed")

    fuel_stations_with_location = add_fuel_station_to_location(serialized_data, user=None)
    print("data processed on t")
    print(fuel_stations_with_location[:10])
    return Response({"data": fuel_stations_with_location}, status=HTTP_200_OK)


#api to get all the state for fuel stations
@api_view(['GET'])
def get_all_station_state(request):
    """
    Fetch all stations and return a list of unique states.
    """
    state_available = check_if_state_cache_exist()

    # Check if all_stations is iterable, if not return an error response or handle it appropriately
    if state_available is None:
        return Response({"error": "Failed to fetch stations"}, HTTP_400_BAD_REQUEST)

    return Response({"data": state_available}, status=HTTP_200_OK)



#api to get all the lga for fuel stations
@api_view(['GET'])
def get_all_station_lga(request):
    """
    Fetch all stations and return a list of unique states.
    """
    lga_available = get_cached_local_governments()
    print(lga_available)

    # Check if all_stations is iterable, if not return an error response or handle it appropriately
    if lga_available is None:
        return Response({"error": "Failed to fetch stations"}, HTTP_400_BAD_REQUEST)

    return Response({"data": lga_available}, status=HTTP_200_OK)

