from datetime import datetime
from dateutil import parser
from deals.models import Deal, Vendor
from distance import in_radius
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
import json


@require_http_methods(["GET"])
def deal(request, deal_id=None, active_only=True):
  """
  @author: Chris
  @desc: Handler for requests to /deal/ and /deals/ endpoints. Routes request
  to appropriate helper function based on request method.

  @param request: the request object
  @param deal_id: deal id to restrict to (optional)
  @param active_only: restricts results to only active deals

  @returns: JSON HttpResponse with any appropriate error codes.
  """
  known_error = None
  deal_set = _get_deals(deal_id, active_only)
  try:
    lat = float(request.GET.get('latitude', None))
    lon = float(request.GET.get('longitude', None))
    radius = float(request.GET.get('radius', -1.0))
  except ValueError:
    lat = None
    lon = None
    radius = -1.0

  deal_list = _list_from_qset(deal_set, include_nested=True)
  deal_list = _limit_result_distance(deal_list, radius, (lat, lon))

  return _make_get_response(deal_list, known_error)

def _get_claimed_deals(vendor_id, active=True):
  """
  by Rahul
  """
  claimed_deal_set = None
  if active:
    claimed_deal_set = Deal.objects.filter(vendor_id=vendor_id,
        claimed_deal__isnull=False, time_end__lte=datetime.now())
  else:
    claimed_deal_set = Deal.objects.filter(vendor_id=vendor_id,
        claimed_deal__isnull=False)
  return claimed_deal_set

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




# TODO implement PUT
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
    vendor, vendor_id = _post_vendor(json.loads(request.body))
    return _make_post_response(vendor, 'vendors/' + str(vendor_id), known_error)
    
@require_http_methods(["GET", "POST"])
def vendor_deals(request, vendor_id):
  if request.method == 'GET':
    known_error = None
    deal_list = None
    if not vendor_id:
      known_error = {'code': 500, 'message': 'Server error'} 
    try:
      deal_set = _get_deals(vendor_id=vendor_id)
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

def _get_deals(deal_id=None, vendor_id=None, active_only=True):
  # A
  """
  @author: Chris, Rahul
  @desc: GET request handler for deals. If deal_id is specified, it retrieves
  the corresponding Deal object and returns the result. Otherwise, response 
  contains an array of all Deal objects. If vendor_id is specified, results are
  limited to deals belonging to that vendor. Setting active_only limits results
  to deals that are currently active. Invalid deal ID's result in an empty QuerySet.

  @param deal_id: deal primary key (integer)
  @param vendor_id: vendor primary key to filter by
  @param active_only: boolean to filter out expired or unstarted deals

  @returns: QuerySet of retrieved objects
  """
  deal_set = None

  if deal_id and vendor_id:
    raise ValueError('[ERR] Func: ideals.views._get_deals | Both deal_id and \
        vendor_id specified')

  if deal_id:
    deal_set = Deal.objects.filter(pk=deal_id)
  else:
    if vendor_id:
      if active_only:
        deal_set = Deal.objects.filter(vendor_id=vendor_id,
            time_end__lte=datetime.now())
      else:
        deal_set = Deal.objects.filter(vendor_id=vendor_id)
    else:
      deal_set = Deal.objects.all()
    if active_only:
      now = datetime.now()
      deal_set = deal_set.filter(time_start__lte=now, time_end__gte=now)
  return deal_set

def _list_from_qset(qset, include_nested=False, flatten=True):
  # A
  """
  @author: Chris
  @desc: Takes a Django QuerySet and from that generates a JSON-serializable list,
  with a form determined by other parameters.

  @param qset: QuerySet to turn into a list
  @param include_nested: Boolean value that decides if foreign object
  information should be included. Only goes through first level.
  @param flatten: Should the list have structure [pk, model, fields = [xyz]] or
                                                    [xyz] (flattened)
  """
  json_data = serializers.serialize("json", qset, use_natural_keys=include_nested)
  obj_list = json.loads(json_data)
  return_list = []

  for obj in obj_list:
    if flatten:
      attrs = obj['fields']
      attrs['id'] = obj['pk'] 
      return_list.append(attrs)
    else:
      return_list.append(obj)
  return return_list

def _limit_result_distance(results, max_radius, loc):
  #A
  """
  @author: Ayush
  @desc: Filters results so that the location for given deals is within
  max_radius of the tuple loc = (latitude, longitude). NOTE: results must be
  flattened.

  @param results: the results we want filtered
  @param max_radius: the radius we are using to filter results
  @param loc: tuple(latitude, longitude) that defines the center of the
  max_radius
  """
  return [x for x in results if in_radius(x['latitude'], x['longitude'], \
      loc[0], loc[1], max_radius)]

def _make_get_response(resp_list, known_error=None):
  #A
  """
  @author: Chris
  @desc: Helper function to take a JSON-serializable list and an optional 
  "known error" dict (with keys 'message' and 'code'), and create an appropriate
  response to a GET request.
  
  @param resp_list: JSON-serializable list to include in GET response
  @param known_error: Any known errors to include/encode in GET response

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

