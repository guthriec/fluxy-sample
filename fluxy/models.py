from django.db import models
from django.contrib.auth.models import AbstractUser

from deals.models import Vendor

class FluxyUser(AbstractUser):
  """
  by Rahul
  This model extends the standard django user model with a phone number and
  many-to-many vendor_id which describes which vendors the user can edit.
  """
  phone = models.CharField(max_length=20)
  vendors = models.ManyToManyField(Vendor)
