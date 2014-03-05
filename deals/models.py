from django.contrib.auth.models import User
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
    image - Link to vendor image
    phone - Phone number
    approved_by - Name of contact we can say approved use of Fluxy 
  """
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  business_type = models.CharField(max_length=100)
  latitude = models.FloatField()
  longitude = models.FloatField()
  web_url = models.URLField()
  yelp_url = models.URLField()
  image = models.ImageField(upload_to='vendors')
  phone = models.CharField(max_length=20)
  approved_by = models.CharField(max_length=100)

  def __unicode__(self):
    """
    Human readable way to print a Vendor instance.
    """
    return self.name

  def natural_key(self):
    """
    For nested serialization.
    """
    return { 
        'id': self.id,
        'name': self.name,
        'address': self.address,
        'business_type': self.business_type,
        'latitude': self.latitude,
        'longitude': self.longitude,
        'web_url': self.web_url,
        'yelp_url': self.yelp_url,
        'image': self.image,
        'phone': self.phone,
        'approved_by': self.approved_by
    } 

class Deal(models.Model):
  """
  Deal model. Here's the schema:
    vendor - Primary 'Vendor' key for the creator of the deal
    title - Short title for the deal
    desc - Longer (500 char) description of the deal
    time_start, time_end - Duration of the deal 
    max_deals - Cap on number of deals available
    instructions - Instructions for users to claim deal at point of sale
  """
  vendor = models.ForeignKey(Vendor)
  title = models.CharField(max_length=40)
  desc = models.CharField(max_length=500)
  time_start = models.DateTimeField()
  time_end = models.DateTimeField()
  max_deals = models.PositiveIntegerField()
  instructions = models.CharField(max_length=1000)

  def __unicode__(self):
    """
    Human readable way to print a Deal instance. e.g. 50% drinks by vendor: Thaiphoon
    """
    return "{0} by vendor: {1}".format(self.title, self.vendor)

class ClaimedDeal(models.Model):
  """
  ClaimedDeal model. Data about a single claimed deal. Schema:
    user - User who claimed the deal
    deal - Deal that's claimed
    time_claimed - Time the user claimed the deal
    claimed_latitude/longitude - Location where the user claimed the deal
    completed - Has the deal been completed?
    time_completed - When was the deal completed?
    completed_latitude/longitude - Location where the deal was completed
  """
  user = models.ForeignKey(User)
  deal = models.ForeignKey(Deal)
  time_claimed = models.DateTimeField(auto_now_add=True)
  claimed_latitude = models.FloatField()
  claimed_longitude = models.FloatField()
  completed = models.BooleanField(default = False)
  time_completed = models.DateTimeField()
  completed_latitude = models.FloatField()
  completed_longitude = models.FloatField()

  def __unicode__(self):
    """
    Human readable way to print a ClaimedDeal instance. 
    """
    return "User {0} claimed deal {1}".format(self.user, self.deal)
