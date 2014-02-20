from deals.models import Deal, Vendor
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def get_deal(deal_id=None):
  """
  GET request handler for deals. If deal_id is specified, it serializes the
  corresponding Deal object to JSON and returns the result. Otherwise, response
  contains an array of all Deal objects. No special handling for invalid deal IDs.
  
  Args: deal primary key (integer)

  Returns: JSON data dump (string)
  """
  if deal_id:
    return serializers.serialize("json", Deal.objects.filter(pk=deal_id))
  else:
    return serializers.serialize("json", Deal.objects.all())

def post_deal(post_dict):
  """
  POST request handler for deals. Adds the specified deal to the DB.
  Assumes the POST request has the following keys, corresponding to field names:
      *vendor (this should be the vendor id)
      *title
      *desc
      *radius
      *time_start
      *time_end

  Args: Django QueryDict consisting of a structured POST request body

  Returns: Nothing. Raises exceptions on error. 
  """
  new_deal = Deal(**post_dict.dict())
  new_deal.save()

def get_vendor(vendor_id=None):
  """
  Behaves identically to get_deal(), except with vendors.
  """
  if vendor_id:
    return serializers.serialize("json", Vendor.objects.filter(pk=vendor_id))
  else:
    return serializers.serialize("json", Vendor.objects.all())

def post_vendor(post_dict):
  """
  POST request handler for vendors. Adds the specified vendor to the DB.
  Assumes the POST request has the following keys, corresponding to field names:
      *name
      *address
      *business_type
      *latitude
      *longitude
      *web_url
      *yelp_url

  Args: Django QueryDict consisting of a structured POST request body

  Returns: Nothing. Raises exceptions on error. 
  """
  new_vendor = Vendor(**post_dict.dict())
  new_vendor.save()

@require_http_methods(["GET", "POST"])
def deal(request, deal_id=None):
  """
  Routes request to appropriate handler based on request method.
  Returns JSON HttpResponse for GET, text for POST (regardless of success).
  """
  if request.method == 'GET':
    resp = get_deal(deal_id)
    return HttpResponse(resp, content_type="application/json")
  else:
    # POST request. Ignore deal_id.
    post_deal(request.POST)
    return HttpResponse("Thanks for submitting!", content_type="text/plain")

@require_http_methods(["GET", "POST"])
def vendor(request, vendor_id=None):
  """
  Routes request to appropriate handler based on request method.
  Returns JSON HttpResponse for GET, text for POST (regardless of success).
  """
  if request.method == 'GET':
    resp = get_vendor(vendor_id)
    return HttpResponse(resp, content_type="application/json")
  else:
    # POST request. Ignore vendor_id.
    post_vendor(request.POST)
    return HttpResponse("Thanks for submitting!", content_type="text/plain")
