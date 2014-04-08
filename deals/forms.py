from deals.models import Vendor
from django.forms import ModelForm

class VendorForm(ModelForm):
  class Meta:
    model = Vendor
