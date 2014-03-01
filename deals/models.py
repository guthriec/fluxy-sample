from django.db import models

class Vendor(models.Model):
  """
  Vendor model. Here's the schema:
    name - vendor name
    address - vendor address
    business_type - category of the business (e.g. restaurant, sports, etc.
                    these categories will eventually be fully defined)
    latitude, longitude - vendor coordinates
    web_url - URL of vendor's website
    yelp_url - URL of vendor's Yelp page
  """
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  business_type = models.CharField(max_length=100)
  latitude = models.FloatField()
  longitude = models.FloatField()
  web_url = models.URLField()
  yelp_url = models.URLField()

  def __unicode__(self):
    """
    Human readable way to print a Vendor instance.
    """
    return self.name

  def natural_key(self):
    """
    For nested serialization.
    """
    return{'id':self.id,\
           'name':self.name,\
           'address':self.address,\
           'business_type':self.business_type,\
           'latitude':self.latitude,\
           'longitude':self.longitude,\
           'web_url':self.web_url,\
           'yelp_url':self.yelp_url} 

class Deal(models.Model):
  """
  Deal model. Here's the schema:
    vendor - Primary 'Vendor' key for the creator of the deal
    title - Short title for the deal
    desc - Longer (500 char) description of the deal
    radius - Distance in miles for the deal to be broadcast
    time_start, time_end - Duration of the deal 
  """
  vendor = models.ForeignKey(Vendor)
  title = models.CharField(max_length=40)
  desc = models.CharField(max_length=500)
  radius = models.PositiveSmallIntegerField()
  time_start = models.DateTimeField()
  time_end = models.DateTimeField()

  def __unicode__(self):
    """
    Human readable way to print a Deal instance. e.g. 50% drinks by vendor: Thaiphoon
    """
    return "{0} by vendor: {1}".format(self.title, self.vendor)
