import datetime
from django.core import serializers
from django.db import models
from django.utils.timezone import utc

class Vendor(models.Model):
  """
  Vendor model. Here's the schema:
    name - vendor name
    address - vendor address
    latitude, longitude - vendor coordinates
    web_url - URL of vendor's website
    yelp_url - URL of vendor's Yelp page
    phone - Phone number
    profile_photo - primary photo for vendor
  """
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  latitude = models.FloatField()
  longitude = models.FloatField()
  web_url = models.URLField()
  yelp_url = models.URLField()
  phone = models.CharField(max_length=20)
  profile_photo = models.ForeignKey('VendorPhoto', related_name='+',
      blank=True, null=True)

  # TODO Validate photo belongs to vendor

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
        'latitude': self.latitude,
        'longitude': self.longitude,
        'web_url': self.web_url,
        'yelp_url': self.yelp_url,
        'phone': self.phone,
        'profile_photo': self.profile_photo.url,
    }


class VendorPhoto(models.Model):
  """
  VendorPhoto model. Schema as follows:
    photo      : The URL of the photo file for this object
    vendor     : The vendor this photo is associated with
    is_primary : A boolean indicating whether this photo is the primary photo
                 for its vendor
  """
  photo = models.ImageField(upload_to='vendors')
  vendor = models.ForeignKey(Vendor)

  def natural_key(self):
    return self.photo.url

  def get_custom_serializable(self):
    return {
          'id': self.id,
          'photo': self.photo.url,
          'vendor': self.vendor.id,
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
    photo - deal specific photo
  """
  vendor = models.ForeignKey(Vendor)
  title = models.CharField(max_length=40)
  desc = models.CharField(max_length=500)
  time_start = models.DateTimeField()
  time_end = models.DateTimeField()
  max_deals = models.PositiveIntegerField(default=100)
  instructions = models.CharField(max_length=1000, default="Show to waiter.")
  photo = models.ForeignKey(VendorPhoto)

  def __unicode__(self):
    """
    Human readable way to print a Deal instance. e.g. 50% drinks by vendor: Thaiphoon
    """
    return "{0} by vendor: {1}".format(self.title, self.vendor)

  def natural_key(self):
    """ For nested serialization. """
    return {
      'id': self.id,
      'title': self.title,
      'desc': self.desc,
      'time_start': self.time_start,
      'time_end': self.time_end,
      'instructions': self.instructions,
    }


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
  user = models.ForeignKey('fluxy.FluxyUser')
  deal = models.ForeignKey(Deal)
  time_claimed = models.DateTimeField(default=datetime.datetime.
                                      utcnow().replace(tzinfo=utc))
  claimed_latitude = models.FloatField(null=True, blank=True)
  claimed_longitude = models.FloatField(null=True, blank=True)
  completed = models.BooleanField(default = False)
  time_completed = models.DateTimeField(null=True, blank=True)
  completed_latitude = models.FloatField(null=True, blank=True)
  completed_longitude = models.FloatField(null=True, blank=True)

  def __unicode__(self):
    """
    Human readable way to print a ClaimedDeal instance.
    """
    return "User {0} claimed deal {1}".format(self.user, self.deal)
