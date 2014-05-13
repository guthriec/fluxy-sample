from deals.models import Vendor
from django.forms import ModelForm

class VendorForm(ModelForm):
  """
  @author: Rahul
  @desc: This is a form class based off the Vendor model used to create and
  process forms that manipulate data for a specific Vendor object.
  """
  class Meta:
    model = Vendor
    fields = ['name', 'address', 'latitude', 'longitude', 'web_url',
        'yelp_url', 'phone', 'profile_photo']

