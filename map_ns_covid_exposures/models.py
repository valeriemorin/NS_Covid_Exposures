from django.contrib.gis.db import models

# Create your models here.

class CovidExposure(models.Model):
    place = models.CharField(max_length=255)
    exposure_from = models.DateTimeField()
    exposure_to = models.DateTimeField()
    address = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    zone = models.CharField(max_length=255)
    last_updated = models.DateTimeField()
    location = models.PointField()
