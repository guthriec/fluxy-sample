import datetime
from deals.distance import distance
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.timezone import utc
from hashlib import sha1
from PIL import Image
from random import random
from sorl.thumbnail import get_thumbnail

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
    profile_photo = None
    if self.profile_photo:
      profile_photo = self.profile_photo.photo.url
    return {
        'id': self.id,
        'name': self.name,
        'address': self.address,
        'latitude': self.latitude,
        'longitude': self.longitude,
        'web_url': self.web_url,
        'yelp_url': self.yelp_url,
        'phone': self.phone,
        'profile_photo': profile_photo
    }


class VendorPhoto(models.Model):
  """
  VendorPhoto model. Schema as follows:
    photo      : The URL of the photo file for this object
    vendor     : The vendor this photo is associated with
    is_primary : A boolean indicating whether this photo is the primary photo
                 for its vendor
  """
  # This creates or returns an extant thumbnail
  def get_thumb(self, dimension_string=None):
    if not dimension_string:
      dimension_string = '400x400'
    return get_thumbnail(self.photo, dimension_string, crop='center',
        quality=99).url

  def natural_key(self):
    return {
        'thumb': self.get_thumb(),
        'deal_thumb': self.get_thumb('320x190'),
        'main_thumb': self.get_thumb('292x150'),
        'claimed_thumb': self.get_thumb('74x74'),
        'photo': self.photo.url
      }

  def get_custom_serializable(self, options):
    return {
          'id': self.id,
          'photo': self.photo.url,
          'thumb': self.get_thumb(),
          'deal_thumb': self.get_thumb('320x190'),
          'main_thumb': self.get_thumb('292x150'),
          'claimed_thumb': self.get_thumb('74x74'),
          'vendor': self.vendor.id,
        }

  def generate_filename(instance, filename):
    return 'vendors/%d/%s_%s.jpg' % (instance.vendor.id,
        datetime.datetime.utcnow().strftime('%s'),
        sha1(str(random())).hexdigest())

  photo = models.ImageField(upload_to=generate_filename)
  vendor = models.ForeignKey(Vendor)


class Deal(models.Model):
  """
  Deal model. Here's the schema:
    vendor - Primary 'Vendor' key for the creator of the deal
    title - Short title for the deal
    subtitle - Longer (40 char) subtitle for the deal
    desc - Longer (500 char) description of the deal
    time_start, time_end - Duration of the deal
    max_deals - Cap on number of deals available
    instructions - Instructions for users to claim deal at point of sale
    photo - deal specific photo
  """
  class Meta:
    ordering = ['time_start']

  # Non-field attributes
  timedelta_prior_to_start_for_active = datetime.timedelta(0,0,0,0,0,6)
  # End

  vendor = models.ForeignKey(Vendor)
  title = models.CharField(max_length=15)
  subtitle = models.CharField(max_length=40)
  desc = models.CharField(max_length=500)
  time_start = models.DateTimeField()
  time_end = models.DateTimeField()
  cancelled = models.BooleanField(default=False)
  max_deals = models.PositiveIntegerField(default=100)
  instructions = models.CharField(max_length=1000, default="Show to waiter.")
  photo = models.ForeignKey(VendorPhoto)

  def get_stage(self):
    if self.cancelled:
      return 4 # cancelled
    tz = self.time_start.tzinfo
    now = datetime.datetime.now(tz)
    if self.time_end < now:
      return 3 # expired
    if self.time_start < now:
      return 2 # live
    if (self.time_start - now) < self.timedelta_prior_to_start_for_active:
      return 1 # active
    return 0 # scheduled

  def __unicode__(self):
    """
    Human readable way to print a Deal instance. e.g. 50% drinks by vendor: Thaiphoon
    """
    return "{0} by vendor: {1}".format(self.title, self.vendor)

  def get_custom_serializable(self, options):
    """
    Note that this uses a class directly from the Django serializer class to serialize
    dates. I got tired of trying to figure out what the default serializer was
    doing and just used parts of the serializer itself.
    Source for DjangoJSONEncoder at:
    https://github.com/django/django/blob/master/django/core/serializers/json.py
    """
    encoder = DjangoJSONEncoder()

    dist = None
    if options and options['latitude'] and options['longitude']:
      dist = distance(options['latitude'], options['longitude'],
          self.vendor.latitude, self.vendor.longitude)

    return {
        'id': self.id,
        'vendor': self.vendor.natural_key(),
        'distance': dist,
        'title': self.title,
        'subtitle': self.subtitle,
        'desc': self.desc,
        'time_start': encoder.default(self.time_start),
        'time_end': encoder.default(self.time_end),
        'stage': self.get_stage(),
        'max_deals': self.max_deals,
        'claimed_count': self.claimeddeal_set.count(),
        'instructions': self.instructions,
        'photo': self.photo.natural_key(),
      }

  def natural_key(self):
    """ For nested serialization. """
    return {
        'id': self.id,
        'title': self.title,
        'subtitle': self.subtitle,
        'desc': self.desc,
        'time_start': self.time_start,
        'time_end': self.time_end,
        'stage': self.get_stage(),
        'max_deals': self.max_deals,
        'claimed_count': self.claimeddeal_set.count(),
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
  class Meta:
    ordering = ['deal__time_start']

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
