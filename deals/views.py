from dateutil import parser 
from deals.fixture_dicts import FixtureDicts
from deals.models import Deal, Vendor
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json

def _get_deal(deal_id=None):
  """
  GET request handler for deals. If deal_id is specified, it serializes the
  corresponding Deal object to JSON and returns the result. Otherwise, response
  contains an array of all Deal objects. No special handling for invalid deal IDs.
  
  Args: deal primary key (integer)

  Returns: JSON data dump (string)
  """
  if deal_id:
    return Deal.objects.filter(pk=deal_id)
  else:
    return Deal.objects.all()

def _post_deal(post_dict):
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

  Returns: new deal object and its database id 
  """
  new_deal = Deal(**post_dict.dict())
  new_deal.time_start = parser.parse(new_deal.time_start)
  new_deal.time_end = parser.parse(new_deal.time_end)
  new_deal.save()
  return new_deal, new_deal.id

def _get_vendor(vendor_id=None):
  """
  Behaves identically to get_deal(), except with vendors.
  """
  if vendor_id:
    return Vendor.objects.filter(pk=vendor_id)
  else:
    return Vendor.objects.all()

def _post_vendor(post_dict):
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

  Returns: new vendor object and its database id.
  """
  new_vendor = Vendor(**post_dict.dict())
  new_vendor.save()
  return new_vendor, new_vendor.id

def _make_get_response(qset, known_error = None):
  if not known_error and qset.count() == 0:
    known_error = {'code': 404, 'message': 'No resource found'}
  if known_error:
    code = known_error['code']
    err_message = known_error['message']
    return HttpResponse(json.dumps(known_error),\
                        content_type="application/json", status=code)
  else:
    return HttpResponse(serializers.serialize("json", qset),\
                        content_type="application/json", status=200)

def _make_post_response(obj, redirect_addr, known_error = None):
  if known_error:
    code = known_error['code']
    err_message = known_error['message']
    return HttpResponse(json.dumps(known_error),\
                        content_type="application/json", status=code)

  else:
    return HttpResponseRedirect(redirect_addr, serializers.serialize("json", [obj]),\
                                content_type="application/json", status=201)

@require_http_methods(["GET", "POST"])
def deal(request, deal_id=None):
  """
  Routes request to appropriate handler based on request method.
  Returns JSON HttpResponse for GET, 201 redirect with JSON for POST
  (regardless of success).
  """
  if request.method == 'GET':
    known_error = None
    deal_set = None
    try:
      deal_set = _get_deal(deal_id)
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_get_response(deal_set, known_error)
  else:
    # POST request.
    known_error = None
    deal = None
    try:
      deal, deal_id = _post_deal(request.POST)
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_post_response(deal, 'deals/' + str(deal_id), known_error)

@require_http_methods(["GET", "POST"])
def vendor(request, vendor_id=None):
  """
  Routes request to appropriate handler based on request method.
  Returns JSON HttpResponse for GET, 201 redirect with JSON for POST
  (regardless of success).
  """
  if request.method == 'GET':
    known_error = None
    vendor_set = None
    try:
      vendor_set = _get_vendor(vendor_id)
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_get_response(vendor_set, known_error)
  else:
    # POST request.
    known_error = None
    vendor = None
    try:
      vendor, vendor_id = _post_vendor(request.POST)
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_post_response(vendor, 'vendors/' + str(vendor_id), known_error)
    
@require_http_methods(["GET"])
def mock_deal(request, deal_id=None):
  deal_set = []
  if deal_id == None:
    deal_set = FixtureDicts.deals
  if deal_id == "1":
    deal_set = [FixtureDicts.deal1]
  if deal_id == "2":
    deal_set = [FixtureDicts.deal2]
  return HttpResponse(json.dumps(deal_set),\
                      content_type="application/json", status=200)

@require_http_methods(["GET"])
def mock_vendor(request, vendor_id=None):
  vendor_set = []
  if vendor_id == None:
    vendor_set = FixtureDicts.vendors
  if vendor_id == "1":
    vendor_set = [FixtureDicts.vendor1]
  if vendor_id == "2":
    vendor_set = [FixtureDicts.vendor2]
  return HttpResponse(json.dumps(vendor_set),\
                      content_type="application/json", status=200)
