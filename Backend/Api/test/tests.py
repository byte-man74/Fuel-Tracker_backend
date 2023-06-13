from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Main.models import Fueling_station, Fuel_Station_Price, Fuel_Station_Traffic_Rating, Fuel_Station_Position, Fuel_Station_Extra_Information


class ViewFuelingStationInformationTest(APITestCase):
    def setUp(self):
        self.fuel_station = Fueling_station.objects.create(
            name='Fuel Station 1')
        self.price = Fuel_Station_Price.objects.create(
            station=self.fuel_station, price=10.99)
        self.traffic_rating = Fuel_Station_Traffic_Rating.objects.create(
            station=self.fuel_station, rating=4)
        self.position = Fuel_Station_Position.objects.create(
            station=self.fuel_station, latitude=1.234, longitude=2.345)
        self.extra_information = Fuel_Station_Extra_Information.objects.create(
            station=self.fuel_station, details='Some extra details')

    def test_get_fueling_station_information(self):
        url = reverse('view-fueling-station-information',
                      args=[self.fuel_station.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['station']['name'], 'Fuel Station 1')
        self.assertEqual(response.data['price']['price'], 10.99)
        self.assertEqual(response.data['traffic_rating']['rating'], 4)
        self.assertEqual(response.data['position']['latitude'], 1.234)
        self.assertEqual(response.data['position']['longitude'], 2.345)
        self.assertEqual(
            response.data['extra_information']['details'], 'Some extra details')
