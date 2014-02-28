from dateutil import parser 
from deals.fixture_dicts import FixtureDicts
from deals.models import Deal, Vendor
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json

def get_deal(deal_id=None):
  """
  by Chris
  GET request handler for deals. If deal_id is specified, it retrieves the
  corresponding Deal object and returns the result. Otherwise, response
  contains an array of all Deal objects. No special handling for invalid deal IDs.
  
  Args: deal primary key (integer)

  Returns: QuerySet of retrieved objects 
  """
  if deal_id:
    return Deal.objects.filter(pk=deal_id)
  else:
    return Deal.objects.all()

def post_deal(post_dict):
  """
  by Chris
  POST request handler for deals. Adds the specified deal to the DB, performing
  required deserialization.
  Assumes the POST request has the following keys, corresponding to field names:
      *vendor (this should be the vendor id)
      *title
      *desc
      *radius
      *time_start
      *time_end

  Args: Django QueryDict consisting of a structured POST request body

  Returns: new deal object and its database id 
  """
  new_deal = Deal(**post_dict.dict())
  new_deal.time_start = parser.parse(new_deal.time_start)
  new_deal.time_end = parser.parse(new_deal.time_end)
  new_deal.save()
  return new_deal, new_deal.id

def get_vendor(vendor_id=None):
  """
  by Chris
  Behaves identically to get_deal(), except with vendors.
  """
  if vendor_id:
    return Vendor.objects.filter(pk=vendor_id)
  else:
    return Vendor.objects.all()

def post_vendor(post_dict):
  """
  POST request handler for vendors. Adds the specified vendor to the DB. Should
  deserialize any necessary fields.
  Assumes the POST request has the following keys, corresponding to field names:
      *name
      *address
      *business_type
      *latitude
      *longitude
      *web_url
      *yelp_url

  Args: Django QueryDict consisting of a structured POST request body

  Returns: new vendor object and its database id
  """
  new_vendor = Vendor(**post_dict.dict())
  new_vendor.save()
  return new_vendor, new_vendor.id

@require_http_methods(["GET", "POST"])
def deal(request, deal_id=None):
  """
  by Chris
  Routes request to appropriate handler based on request method.
  Returns JSON HttpResponse for GET, 201 redirect with JSON for POST
  (regardless of success).
  """
  if request.method == 'GET':
    deal_set = get_deal(deal_id)
    return HttpResponse(serializers.serialize("json", deal_set),\
                        content_type="application/json", status=200)
  else:
    # POST request. Ignore deal_id.
    deal, deal_id = post_deal(request.POST)
    return HttpResponseRedirect('deals/' + str(deal_id),\
                                serializers.serialize("json", [deal]),\
                                content_type="application/json", status=201)

@require_http_methods(["GET", "POST"])
def vendor(request, vendor_id=None):
  """
  by Chris
  Routes request to appropriate handler based on request method.
  Returns JSON HttpResponse for GET, 201 redirect with JSON for POST
  (regardless of success).
  """
  if request.method == 'GET':
    vendor_set = get_vendor(vendor_id)
    return HttpResponse(serializers.serialize("json", vendor_set),\
                        content_type="application/json", status=200)
  else:
    # POST request. Ignore vendor_id.
    vendor, vendor_id = post_vendor(request.POST)
    return HttpResponseRedirect('vendors/' + str(vendor_id),\
                                serializers.serialize("json", [vendor]),\
                                content_type="application/json", status=201)

@require_http_methods(["GET"])
def mock_deal(request, deal_id=None):
  """
  by Chris
  Short-circuits the database to return a mock JSON deal set.
  """
  deal_set = []
  deal1_full = Deal(pk=1, **FixtureDicts.deal1)
  deal2_full = Deal(pk=2, **FixtureDicts.deal2)
  if deal_id == None:
    deal_set = [deal1_full, deal2_full] 
  if deal_id == "1":
    deal_set = [deal1_full] 
  if deal_id == "2":
    deal_set = [deal2_full]
  return HttpResponse(serializers.serialize("json", deal_set),\
                      content_type="application/json", status=200)

@require_http_methods(["GET"])
def mock_vendor(request, vendor_id=None):
  """
  by Chris
  Short-circuits the database to return a mock JSON vendor set.
  """
  vendor_set = []
  vendor1_full = Vendor(pk=1, **FixtureDicts.vendor1)
  vendor2_full = Vendor(pk=2, **FixtureDicts.vendor2)
  if vendor_id == None:
    vendor_set = [vendor1_full, vendor2_full] 
  if vendor_id == "1":
    vendor_set = [vendor1_full] 
  if vendor_id == "2":
    vendor_set = [vendor2_full]
  return HttpResponse(serializers.serialize("json", vendor_set),\
                      content_type="application/json", status=200)
