from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import CovidExposure


@admin.register(CovidExposure)
class CovidExposureAdmin(OSMGeoAdmin):
    list_display = ('place', 'address', 'type', 'zone', 'last_updated')
