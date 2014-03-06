from datetime import datetime
from dateutil import parser
from deals.fixture_dicts import FixtureDicts
from deals.models import Deal, Vendor
from distance import in_radius
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json

def dashboard(request):
  return render(request, 'deals/dashboard.html')

def _get_deal(deal_id=None, vendor_id=None, active_only=True):
  """
  @author: Chris

  @desc: GET request handler for deals. If deal_id is specified, it retrieves the
  corresponding Deal object and returns the result. Otherwise, response
  contains an array of all Deal objects. If vendor_id is specified, results
  are limited to deals belonging to that vendor. Setting active_only limits
  results to deals that are currently active.
  Invalid deal ID's result in an empty QuerySet.

  @params: deal_id: deal primary key (integer)
           vendor_id: vendor primary key to filter by
           active_only: boolean to filter out expired or unstarted deals

  @returns: QuerySet of retrieved objects
  """
  deal_set = None
  if deal_id and vendor_id:
    raise ValueError("You done gone goofed")
  if deal_id:
    deal_set = Deal.objects.filter(pk=deal_id)
  else:
    if vendor_id:
      deal_set = Deal.objects.filter(vendor_id=vendor_id)
    else:
      deal_set = Deal.objects.all()
    if active_only:
      now = datetime.now()
      deal_set = deal_set.filter(time_start__lte=now, time_end__gte=now)
  return deal_set

def _get_vendor(vendor_id=None):
  """
  by Chris
  Behaves identically to _get_deal(), except with vendors.
  """
  vendor_set = None
  if vendor_id:
    vendor_set = Vendor.objects.filter(pk=vendor_id)
  else:
    vendor_set = Vendor.objects.all()
  return vendor_set

def _post_deal(post_dict):
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

  Args: Dict consisting of a structured POST request body

  Returns: new deal object and its database id
  """
  new_deal = Deal(**post_dict)
  new_deal.time_start = parser.parse(new_deal.time_start)
  new_deal.time_end = parser.parse(new_deal.time_end)
  new_deal.save()
  return new_deal, new_deal.id

def _post_vendor(post_dict):
  """
  by Chris
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

  Args: Dict consisting of a structured POST request body

  Returns: new vendor object and its database id.
  """
  new_vendor = Vendor(**post_dict)
  new_vendor.save()
  return new_vendor, new_vendor.id

def _list_from_qset(qset, include_nested=False, flatten=True, max_radius=-1, loc=None):
  """
  @author: Chris

  @desc: Takes a Django QuerySet and from that generates a JSON-serializable list,
         with a form determined by other parameters.

  @params: qset - QuerySet to turn into a list
           include_nested - Should the list include information about associated
                            foreign objects?
           flatten - Should the list have structure [pk, model, fields = [xyz]] or
                                                    [xyz] (flattened)
           max_radius, loc - If both are set, filters results so that the location
                             specified by fields['lat'] and fields['long'] is within
                             max_radius of tuple loc = (latitude, longitude)
  """
  json_out = serializers.serialize("json", qset, use_natural_keys=include_nested)
  if flatten:
    obj_list = json.loads(json_out)
    flattened = []
    for obj in obj_list:
      attrs = obj['fields']
      if max_radius >= 0 and loc:
        lat = attrs['lat']
        lon = attrs['long']
        if not in_radius(lat, lon, loc[0], loc[1], max_radius):
          continue
      flattened.append(attrs)

def _make_get_response(resp_list, known_error=None):
  """
  @author: Chris
  
  @desc: Helper function to take a JSON-serializable list and an optional "known error"
         dict (with keys 'message' and 'code'), and create an appropriate
         response to a GET request.
  
  @params: resp_list - JSON-serializable list to include in GET response
           known_error - Any known errors to include/encode in GET response

  @returns: JSON HttpResponse with status 200 on success
            JSON HttpResponse with appropriate error code if known_error
  """
  if known_error:
    code = known_error['code']
    err_message = known_error['message']
    return HttpResponse(json.dumps(known_error),\
                        content_type="application/json", status=code)
  else:
    json_out = json.dumps(resp_list)
    return HttpResponse(json_out, content_type="application/json", status=200)

def _make_post_response(obj, redirect_addr, known_error = None):
  """
  As with _make_get_response, generates an appropriate response given
  any known errors passed in, along with the created object and an
  address to redirect to.
  """
  if known_error:
    code = known_error['code']
    err_message = known_error['message']
    return HttpResponse(json.dumps(known_error),\
                        content_type="application/json", status=code)
  else:
    return HttpResponseRedirect(redirect_addr, serializers.serialize("json", [obj]),\
                                content_type="application/json", status=201)



@require_http_methods(["GET"])
def deal(request, deal_id=None, active_only=True):
  """
  @author: Chris

  @desc: Handler for requests to /deal/ and /deals/ endpoints.
        Routes request to appropriate helper function based on request method.

  @params: request, optional deal_id
           active_only - restricts results to only active deals

  @returns: JSON HttpResponse with any appropriate error codes.
  """
  known_error = None
  deal_set = _get_deal(deal_id, active_only)
  try:
    lat = float(request.GET.get('lat', None))
    lon = float(request.GET.get('long', None))
    radius = float(request.GET.get('radius', -1.0))
  except ValueError:
    lat = None
    lon = None
    radius = -1.0
  deal_list = _list_from_qset(deal_set, include_nested=True,\
                              max_radius = radius, loc = (lat, lon))
  return _make_get_response(deal_list, known_error)

@require_http_methods(["GET", "POST"])
def vendor(request, vendor_id=None):
  """
  by Chris
  Routes request to appropriate handler based on request method.
  Returns JSON HttpResponse for GET, 201 redirect with JSON for POST
  (regardless of success).
  """
  if request.method == 'GET':
    known_error = None
    vendor_list = None
    try:
      vendor_set = _get_vendor(vendor_id)
      vendor_list = _list_from_qset(vendor_set, include_nested=False)
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_get_response(vendor_list, known_error,\
                              flatten=True, include_nested=False)
  else:
    # POST request.
    known_error = None
    vendor = None
    try:
      vendor, vendor_id = _post_vendor(json.loads(request.body))
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_post_response(vendor, 'vendors/' + str(vendor_id), known_error)
    
@require_http_methods(["GET", "POST"])
def vendor_deals(request, vendor_id):
  if request.method == 'GET':
    known_error = None
    deal_list = None
    if not vendor_id:
      known_error = {'code': 500, 'message': 'Server error'} 
    try:
      deal_set = _get_deal(vendor_id=vendor_id)
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    deal_list = _list_from_qset(deal_set, include_nested=True)
    return _make_get_response(deal_list, known_error,\
                              flatten=True, include_nested=True)
  else:
    known_error = None
    deal = []
    deal_id = -1
    try:
      deal, deal_id = _post_deal(json.loads(request.body))
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_post_response(deal, 'deals/' + str(deal_id), known_error)

@require_http_methods(["GET"])
def mock_deal(request, deal_id=None):
  """
  by Chris
  Short-circuits the database to return a mock JSON deal set.
  """
  deal_set = []
  deal1_full = FixtureDicts.deal1
  deal2_full = FixtureDicts.deal2
  if deal_id == None:
    deal_set = [deal1_full, deal2_full]
  if deal_id == "1":
    deal_set = [deal1_full]
  if deal_id == "2":
    deal_set = [deal2_full]
  for obj in deal_set:
    obj['vendor'] = FixtureDicts.vendor1
  return HttpResponse(json.dumps(deal_set), content_type="application/json", status=200)

@require_http_methods(["GET"])
def mock_vendor(request, vendor_id=None):
  """
  by Chris
  Short-circuits the database to return a mock JSON vendor set.
  """
  vendor_set = []
  vendor1_full = FixtureDicts.vendor1
  vendor2_full = FixtureDicts.vendor2
  if vendor_id == None:
    vendor_set = [vendor1_full, vendor2_full]
  if vendor_id == "1":
    vendor_set = [vendor1_full]
  if vendor_id == "2":
    vendor_set = [vendor2_full]
  return HttpResponse(json.dumps(vendor_set), content_type="application/json", status=200)
