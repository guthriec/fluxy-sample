from dateutil import parser
from deals.fixture_dicts import FixtureDicts
from deals.models import Deal, Vendor
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
import json

def _get_deal(deal_id=None, vendor_id=None):
  """
  by Chris
  GET request handler for deals. If deal_id is specified, it retrieves the
  corresponding Deal object and returns the result. Otherwise, response
  contains an array of all Deal objects. Invalid deal ID's result in
  an empty QuerySet.

  Args: deal primary key (integer)

  Returns: QuerySet of retrieved objects
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

def _make_get_response(qset, known_error=None, include_nested=False, flatten=True):
  """
  by Chris
  Helper function to take a QuerySet and an optional "known error"
  dict (with keys 'message' and 'code'), and create an appropriate
  response to a GET request.
  """
  if known_error:
    code = known_error['code']
    err_message = known_error['message']
    return HttpResponse(json.dumps(known_error),\
                        content_type="application/json", status=code)
  else:
    json_out = serializers.serialize("json", qset, use_natural_keys=include_nested)
    if flatten:
      obj_list = json.loads(json_out)
      flattened = []
      for obj in obj_list:
        flattened.append(obj['fields'])
      json_out = json.dumps(flattened)
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

@require_http_methods(["GET", "POST"])
def deal(request, deal_id=None):
  """
  by Chris
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
    return _make_get_response(deal_set, known_error, include_nested=True)
  else:
    # POST request.
    known_error = None
    deal = None
    try:
      deal, deal_id = _post_deal(json.loads(request.body))
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_post_response(deal, 'deals/' + str(deal_id), known_error)

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
    vendor_set = None
    try:
      vendor_set = _get_vendor(vendor_id)
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_get_response(vendor_set, known_error,\
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
    deal_set = None
    if not vendor_id:
      known_error = {'code': 500, 'message': 'Server error'} 
    try:
      deal_set = _get_deal(vendor_id=vendor_id)
    except Exception:
      known_error = {'code': 500, 'message': 'Server error'}
    return _make_get_response(deal_set, known_error,\
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
