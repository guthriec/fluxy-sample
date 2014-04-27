from datetime import datetime
from dateutil import parser
from deals.api_tools import make_get_response, make_post_response, make_put_response, list_from_qset
from deals.decorators import api_login_required, api_vendor_required
from deals.models import ClaimedDeal, Deal, Vendor
from distance import in_radius
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
def deal(request, deal_id=None, active_only=True):
  """
  @author: Chris, Ayush
  @desc: Handler for requests to /deal/ and /deals/ endpoints. Routes request
  to appropriate helper function based on request method.

  @param request: the request object
  @param deal_id: deal id to restrict to (optional)
  @param active_only: restricts results to only active deals

  @return: JSON HttpResponse with any appropriate error codes.
  """
  known_error = None
  if deal_id:
    active_only = False
  deal_set = _get_deals(deal_id, active_only=active_only)
  if deal_id and deal_set.count() == 0:
    known_error = { 'code': 404, 'message': 'Deal not found' }
  try:
    lat = float(request.GET.get('latitude', None))
    lon = float(request.GET.get('longitude', None))
    radius = float(request.GET.get('radius', -1.0))
  except TypeError:
    lat = None
    lon = None
    radius = -1.0

  deal_list = list_from_qset(deal_set, include_nested=True)
  deal_list = _limit_result_distance(deal_list, radius, (lat, lon))

  return make_get_response(deal_list, known_error)

@csrf_exempt
@require_http_methods(["GET", "POST"])
@api_login_required(["POST"])
def vendor(request, vendor_id=None):
  """
  @TODO: Implement PUT
  @author: Chris, Ayush
  @desc: Routes request to appropriate handler based on request method. Returns
  JSON HttpResponse for GET, 201 redirect with JSON for POST (regardless of
  success). Returns/creates vendor objects
  Assumes the POST request has the following keys, corresponding to field names:
      *name
      *address
      *latitude
      *longitude
      *web_url
      *yelp_url

  @param request: the request object
  @param vendor_id: the vendor id we are querying. None if POST

  @return: 201 with JSON for POST or 200 for GET
  """
  if request. method == 'GET':
    known_error = None
    vendor_list = None
    vendor_set = _get_vendor(vendor_id)
    if vendor_id and vendor_set.count() == 0:
      known_error = { 'code': 404, 'message': 'Vendor not found' }
      return make_get_response(vendor_list, known_error)

    vendor_list = list_from_qset(vendor_set, include_nested=False, flatten=True)
    return make_get_response(vendor_list, known_error)
  else:
    # POST request.
    known_error = None
    vendor_list = None
    vendor_id = -1
    try:
      vendor = Vendor(**json.loads(request.body))
      vendor.save()
      vendor_id = str(vendor.id)
      vendor_list = list_from_qset([vendor])
    except TypeError:
      known_error = { 'code': 400, 'message': 'Bad post request' }
    return make_post_response(vendor_list, 'vendors/' + str(vendor_id), known_error)

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT"])
@api_vendor_required(["POST"])
def vendor_deals(request, vendor_id, deal_id=None, active_only=True):
  """
  @author: Chris, Ayush
  @desc: Returns/creates/edits a deal or set of deals for a given vendor
  Assumes the POST request has the following keys, corresponding to field names:
      *vendor (this should be the vendor id)
      *title
      *desc
      *time_start
      *time_end

  @param request: a request object
  @param vendor_id: the id of the vendor for which we are querying or creating
  a deal for
  @param deal_id: the deal_id of the deal (for PUT)
  @param active_only: boolean to filter GET results to active deals

  @return: 201 with JSON for POST or 200 with JSON for GET/PUT
  """
  known_error = None
  deal_list = None

  # Check vendor exists
  vendor_qset = Vendor.objects.filter(pk=vendor_id)
  if vendor_qset.count() == 0:
    known_error = { 'code': 404, 'message': 'Vendor not found' }
    return make_get_response(deal_list, known_error)

  if request.method == 'GET':
    # ---- GET ----
    deal_set = _get_deals(vendor_id=vendor_id, active_only=active_only)
    deal_list = list_from_qset(deal_set, include_nested=True)
    return make_get_response(deal_list, known_error)
  
  elif request.method == 'PUT':
    # ---- PUT ----
    deal = None
    try:
      deal = Deal.objects.get(pk=deal_id)
    except Deal.DoesNotExist:
      known_error = { 'code': 404, 'message': 'Deal not found' }
      return make_put_response(None, 'deals/' + str(deal_id), known_error)
    updates = json.loads(request.body)
    for key, val in updates.iteritems():
      try:
        getattr(deal, key)
      except AttributeError:
        known_error = { 'code' : 400, 'message': 'Bad PUT request for deal' }
        return _make_put_response(None, 'deals/' + str(deal_id), known_error)
      setattr(deal, key, val) 
    deal.save()
    single_deal_list = list_from_qset([deal], flatten=True, include_nested=False)
    return _make_put_response(single_deal_list, 'deals/' + str(deal_id), known_error)
  
  else:
    # ---- POST ----
    deal = None
    deal_id = -1
    try:
      deal = Deal(**json.loads(request.body))
      deal.vendor_id = vendor_id
      deal.time_start = parser.parse(deal.time_start)
      deal.time_end = parser.parse(deal.time_end)
      deal.save()
      deal_id = deal.id
      deal_list = list_from_qset([deal])
    except Exception:
      known_error={ 'code': 400, 'message': 'Bad deal POST' }
    return make_post_response(deal_list, 'deals/' + str(deal_id), known_error)

@require_http_methods(['GET'])
@api_vendor_required(['GET'])
def vendor_claimed_deals(request, vendor_id, active_only=True):
  """
  @author: Chris
  @param vendor_id: vendor primary key
  @param active_only: boolean to filter out expired or unstarted deals

  @returns JSON response
  """
  known_error = None
  claimed_deal_list = None

  vendor_set = Vendor.objects.filter(pk=vendor_id)
  if vendor_set.count() == 0:
    known_error = { 'code': 404, 'message': 'Vendor not found' }
    return make_get_response(claimed_deal_list, known_error)
  claimed_deal_set = _get_claimed_deals(vendor_id=vendor_id, active_only=active_only)
  claimed_deal_list = list_from_qset(claimed_deal_set, include_nested=False, flatten=True)
  return make_get_response(claimed_deal_list, known_error)


def _get_claimed_deals(claimed_deal_id=None, vendor_id=None, active_only=True):
  """
  @author: Chris
  @desc: GET request handler for ClaimedDeals. Applies filters specified by parameters
  to ClaimedDeal objects, returning what's left (so invalid deal ID's result in an
  empty QuerySet).

  @param claimed_deal_id: claimed deal primary key
  @param vendor_id: vendor primary key to filter by
  @param active_only: boolean to filter out expired or unstarted deals

  @returns: QuerySet of retrieved objects
  """
  claimed_deal_set = ClaimedDeal.objects.all()
  if vendor_id:
    claimed_deal_set = claimed_deal_set.filter(deal__vendor_id=vendor_id)
  if claimed_deal_id:
    claimed_deal_set = claimed_deal_set.filter(pk=claimed_deal_id)
  if active_only:
    now = datetime.utcnow().replace(tzinfo=utc)
    claimed_deal_set = claimed_deal_set.filter(deal__time_start__lte=now,
                                               deal__time_end__gte=now)
  return claimed_deal_set

def _get_deals(deal_id=None, vendor_id=None, active_only=True):
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
  deal_set = Deal.objects.all()
  if deal_id:
    deal_set = deal_set.filter(pk=deal_id)
  if vendor_id:
    deal_set = deal_set.filter(vendor_id=vendor_id)
  if active_only:
    now = datetime.utcnow().replace(tzinfo=utc)
    deal_set = deal_set.filter(time_start__lte=now, time_end__gte=now)
  return deal_set

def _limit_result_distance(results, max_radius, loc):
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
  return [x for x in results if in_radius(x['vendor']['latitude'], x['vendor']['longitude'], \
      loc[0], loc[1], max_radius)]

def _get_vendor(vendor_id=None):
  """
  @author: Ayush, Chris
  @desc: returns a QuerySet of vendors. Filtered to a specific PK if passed in
  as vendor_id.

  @param vendor_id: the vendor_id we want to filter to
  @return QuerySet of vendors
  """
  vendor_set = None
  if vendor_id:
    vendor_set = Vendor.objects.filter(pk=vendor_id)
  else:
    vendor_set = Vendor.objects.all()
  return vendor_set
