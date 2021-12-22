from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import CovidExposure


@admin.register(CovidExposure)
class CovidExposureAdmin(OSMGeoAdmin):
    list_display = ('place', 'exposure_from', 'exposure_to', 'address', 'type', 'zone', 'last_updated', 'location')

