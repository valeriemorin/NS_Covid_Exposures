from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import CovidExposure

latitude = 44.94618
longitude = -65.07206

user_location = Point(longitude, latitude, srid=4326)


# Create your views here.
class Home(generic.ListView):
    model = CovidExposure
    context_object_name = "covid_exposures"
    queryset = CovidExposure.objects.annotate(distance=Distance("location", user_location)).order_by("distance")
    template_name = "covid_exposures/index.html"
