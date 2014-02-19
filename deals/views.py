from deals.models import Deal, Vendor
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

@require_GET
def deal(request, deal_id=None):
  """
  Request handler for deals. Currently only handles GET requests. 
  If deal_id is specified, it serializes the
  corresponding Deal object to JSON and returns the result in an HttpResponse.
  If no id is specified, the HttpResponse contains JSON for an array of all
  Deal objects. No special handling for invalid deal IDs.
  """
  if deal_id:
    print Deal.objects.get(pk=deal_id)
    deal = serializers.serialize("json", Deal.objects.filter(pk=deal_id))
    return HttpResponse(deal, content_type="application/json")
  else:
    all_deals = serializers.serialize("json", Deal.objects.all())
    return HttpResponse(all_deals, content_type="application/json")

@require_GET
def vendor(request, vendor_id=None):
  """
  Request handler for vendors. Currently only handles GET requests.
  If vendor_id is specified, it serializes the
  corresponding Vendor object to JSON and returns the result in an HttpResponse.
  If no id is specified, the HttpResponse contains JSON for an array of all
  Vendor objects. No special handling for invalid vendor IDs.
  """
  if vendor_id:
    vendor = serializers.serialize("json", Vendor.objects.filter(pk=vendor_id))
    return HttpResponse(vendor, content_type="application/json")
  else:
    all_vendors = serializers.serialize("json", Vendor.objects.all())
    return HttpResponse(all_vendors, content_type="application/json")
