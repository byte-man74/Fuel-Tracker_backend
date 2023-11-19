from Api.Application_api.helper_function.main_function_support import *
from Api.serializers import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q



@api_view(['GET'])
def get_all_the_stations (request):
    all_stations = check_if_fueling_station_is_in_cache()


    search_query = request.query_params.get('search', None)
    if search_query:
        all_stations = all_stations.filter(
            Q(name__icontains=search_query)  
            #| Q(state__icontains=search_query) |  # Search by state
            # Q(local_government__icontains=search_query)  # Search by local government
        )

    paginator = PageNumberPagination()
    paginator.page_size = 7

    paginated_result = paginator.paginate_queryset(all_stations, request)


    serializer = FuelStationSerializer(paginated_result, many=True)


    serialized_data = serializer.data
    print("data processed")

    fuel_stations_with_location = add_fuel_station_to_location(serialized_data, user=None)
    print("data processed on t")
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

    # Check if all_stations is iterable, if not return an error response or handle it appropriately
    if lga_available is None:
        return Response({"error": "Failed to fetch stations"}, HTTP_400_BAD_REQUEST)

    return Response({"data": lga_available}, status=HTTP_200_OK)

