from django.db import models
from django.contrib.auth.models import AbstractUser

from deals.models import Vendor

class FluxyUser(AbstractUser):
  """
  @author: Rahul
  @desc: This model extends the standard django user model with a phone number and
  many-to-many vendor_id which describes which vendors the user can edit.
  """
  phone = models.CharField(max_length=20, blank=True)
  vendors = models.ManyToManyField(Vendor, blank=True)

  def get_safe_user(self):
    """
    @author: Rahul
    @desc: This returns the properties of the user that can be safely returned
    to the client.

    @return: A dict with the user's first_name, last_name, email, and phone.
    """
    user = {
        'first_name'   : self.first_name,
        'last_name'    : self.last_name,
        'email'        : self.email,
        'phone'        : self.phone,
        'vendors'      : [x['id'] for x in self.vendors.all().values('id')],
    }

    return user
