from django.apps import apps
from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import CovidExposure
from django.contrib.gis.geos import fromstr

latitude = 44.94618
longitude = -65.07206

user_location = Point(longitude, latitude, srid=4326)

DATA_FILENAME = 'data.txt'


def load_data():

    covid_exposure = apps.get_model('map_ns_covid_exposures', 'CovidExposure')

    file = open(DATA_FILENAME, "r")
    for line in file:

        fields = line.split("\",\"")

        place = fields[0].strip("\"")
        exposure_from = fields[1].strip("\"")
        exposure_to = fields[2].strip("\"")

        address = fields[3].strip("\"")
        exposure_type = fields[4].strip("\"")
        zone = fields[5].strip("\"")
        last_updated = fields[6].strip("\"")

        location = fromstr("POINT(%s %s)" % (fields[8].strip("\"\n"), fields[7].strip("\"")), srid=4326)

        covid_exposure(place=place, exposure_from=exposure_from, exposure_to=exposure_to, address=address,
                       type=exposure_type, zone=zone, last_updated=last_updated, location=location).save()

    file.close()


# Create your views here.
class Home(generic.ListView):

    model = CovidExposure

    # Delete contents of the covid exposure table
    model.objects.all().delete()

    # Load the data from the csv
    load_data()

    context_object_name = "covid_exposures"
    queryset = CovidExposure.objects.annotate(distance=Distance("location", user_location)).order_by("distance")
    template_name = "covid_exposures/index.html"



