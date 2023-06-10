from django.contrib import admin
from .models import *


class Fuel_station_price_inline(admin.StackedInline):
    model = Fuel_Station_Price
    can_delete = False
    verbose_name_plural = 'Fuel Station Price'


class Fuel_station_position_inline(admin.StackedInline):
    model = Fuel_Station_Position
    can_delete = False
    verbose_name_plural = 'Fuel Station Position'


class Fuel_Station_Traffic_Rating_inline(admin.StackedInline):
    model = Fuel_Station_Traffic_Rating
    can_delete = False
    verbose_name_plural = 'Fuel Station Traffic Rating'


class Fuel_Station_Extra_Information_inline(admin.StackedInline):
    model = Fuel_Station_Extra_Information
    can_delete = False
    verbose_name_plural = 'Fuel Station Extra Informtion'



class Fueling_station_Admin(admin.ModelAdmin):
    inlines = (Fuel_station_price_inline, Fuel_station_position_inline,
               Fuel_Station_Traffic_Rating_inline, Fuel_Station_Extra_Information_inline)


admin.site.register(Fueling_station, Fueling_station_Admin)
