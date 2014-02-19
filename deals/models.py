from django.db import models

class Vendor(models.Model):
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  business_type = models.CharField(max_length=100)
  latitude = models.FloatField()
  longitude = models.FloatField()
  web_url = models.URLField()
  yelp_url = models.URLField()

class Deal(models.Model):
  vendor = models.ForeignKey(Vendor)
  title = models.CharField(max_length=40)
  desc = models.CharField(max_length=500)
  radius = models.PositiveSmallIntegerField()
  time_start = models.DateTimeField()
  time_end = models.DateTimeField()

