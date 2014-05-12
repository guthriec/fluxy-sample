from datetime import datetime
from dateutil import parser
from deals.api_tools import make_get_response, make_delete_response, \
                            make_post_response, make_put_response, \
                            list_from_qset, custom_serialize
from deals.decorators import api_login_required, api_vendor_required
from deals.models import ClaimedDeal, Deal, Vendor, VendorPhoto
from deals.forms import VendorForm
from distance import in_radius
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render, get_object_or_404
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
    known_error = { 'status': 404, 'detail': 'Deal not found' }
  try:
    lat = float(request.GET.get('latitude', None))
    lon = float(request.GET.get('longitude', None))
    radius = float(request.GET.get('radius', -1.0))
  except TypeError:
    lat = None
    lon = None
    radius = -1.0

  deal_list = custom_serialize(deal_set, {
      'latitude': lat,
      'longitude': lon
    })
  deal_list = _limit_result_distance(deal_list, radius, (lat, lon))

  return make_get_response(deal_list, known_error)

@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT'])
@api_login_required(['POST', 'PUT'])
@api_vendor_required(['PUT'])
def vendor(request, vendor_id=None):
  """
  @author: Chris, Ayush, Rahul
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
  if request.method == 'GET':
    known_error = None
    vendor_list = None
    vendor_set = _get_vendor(vendor_id)
    if vendor_id and vendor_set.count() == 0:
      known_error = { 'status': 404, 'detail': 'Vendor not found.' }
      return make_get_response(vendor_list, known_error)

    vendor_list = list_from_qset(vendor_set, include_nested=False, flatten=True)
    return make_get_response(vendor_list, known_error)
  else:
    try:
      data = json.loads(request.body)
      known_error = None
      vendor_form = None
      if request.method == 'POST':
        vendor_form = VendorForm(data)
        vendor = vendor_form.save()
        vendor_id = str(vendor.id)
        vendor_list = list_from_qset([vendor])
        return make_post_response(vendor_list, 'vendors/' + str(vendor_id),
            known_error)
      else: # PUT
        vendor = Vendor.objects.get_object_or_404(pk = vendor_id)
        vendor_form = VendorForm(data, instance=vendor)
        vendor = vendor_form.save()
        vendor_id = str(vendor.id)
        return HttpResponse(serializers.serialize('json', [vendor]),
            content_type='application/json')
    except (TypeError, ValueError), e:
      known_error = { 'status': 400, 'error': 'Bad request.' }
      return make_post_response(vendor, 'vendors/' + str(vendor_id), known_error)

@csrf_exempt
@require_http_methods(['GET', 'POST', 'DELETE'])
@api_login_required(['GET', 'POST', 'DELETE'])
@api_vendor_required(['GET', 'POST', 'DELETE'])
def vendor_photo(request, vendor_id, photo_id=None):
  """
  @author: Rahul
  @desc: Creates a new VendorPhoto object and associates it with the specified
  vendor. Does NOT make the photo the vendor's primary photo. Requires the user
  to be authenticated and have vendor permissions.

  @param request: the request object
  @param vendor_id: the id of the vendor to associate the photo with.

  @return: a 201 response with the JSON encoded VendorPhoto object

  TODO Validate POSTed filetype
  """
  vendor = get_object_or_404(Vendor, pk=vendor_id)
  if request.method == 'GET':
    return make_get_response(custom_serialize(vendor.vendorphoto_set.all()))
  elif request.method == 'POST':
    try:
      vendor_photo = VendorPhoto(photo=request.FILES['photo'],
          vendor=vendor)
      vendor_photo.save()
    except:
      return HttpResponse(json.dumps({ 'status': 400, 'error': 'Bad request.' }),
        content_type='application/json', status=400)
    return make_post_response(custom_serialize([vendor_photo]))
  else:
    vendor_photo = get_object_or_404(VendorPhoto, pk=photo_id)
    vendor_photo.photo.delete()
    vendor_photo.delete()
    return HttpResponse(json.dumps({'status': 200,
        'detail': 'Successfully deleted photo.'}))

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
@api_vendor_required(["POST", "PUT", "DELETE"])
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
    known_error = { 'status': 404, 'detail': 'Vendor not found' }
    return make_get_response(deal_list, known_error)

  if request.method == 'GET':
    # ---- GET ----
    deal_set = _get_deals(vendor_id=vendor_id, active_only=active_only)
    deal_list = custom_serialize(deal_set)
    return make_get_response(deal_list, known_error)

  elif request.method == 'PUT':
    # ---- PUT ----
    deal = None
    try:
      deal = Deal.objects.get(pk=deal_id)
    except Deal.DoesNotExist:
      known_error = { 'status': 404,
                      'error': 'Resource not found',
                      'detail': 'No deal of specified id exists' }
      return make_put_response(None, known_error)
    updates = json.loads(request.body)
    for key, val in updates.iteritems():
      try:
        getattr(deal, key)
      except AttributeError:
        known_error = { 'status' : 400,
                        'error': 'Bad PUT request',
                        'detail': '''PUT request tried to update a
                                   non-existent attribute''' }
        return make_put_response(None, known_error)
      setattr(deal, key, val)
    deal.save()
    single_deal_list = custom_serialize([deal])
    return make_put_response(single_deal_list, known_error)

  elif request.method == 'POST':
    # ---- POST ----
    deal = None
    deal_id = -1
    try:
      post_data = json.loads(request.body)
      # TODO validate photo belongs to vendor
      photo = VendorPhoto.objects.get(pk=post_data['photo']['id']);
      post_data['photo'] = photo
      deal = Deal(**post_data)
      deal.vendor_id = vendor_id
      deal.time_start = parser.parse(deal.time_start)
      deal.time_end = parser.parse(deal.time_end)
      deal.save()
      deal_id = deal.id
      deal_list = custom_serialize([deal])
    except Exception:
      known_error={ 'status': 400, 'detail': 'Bad deal POST' }
    return make_post_response(deal_list, 'deals/' + str(deal_id), known_error)
  else:
    # ---- DELETE ----
    try:
      deal = Deal.objects.get(pk=deal_id)
      deal.cancelled = True
      deal.save()
    except Deal.DoesNotExist:
      known_error = { 'status': 404,
                      'error': 'Resource not found',
                      'detail': 'No deal of specified id exists' }
    return make_delete_response(known_error)

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
    known_error = { 'status': 404, 'detail': 'Vendor not found' }
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
    now = datetime.now(utc)
    claimed_deal_set = claimed_deal_set.filter(deal__time_start__lte=now +
        Deal.timedelta_prior_to_start_for_active, deal__time_end__gte=now)
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
    now = datetime.now(utc)
    deal_set = deal_set.filter(time_start__lte=now +
        Deal.timedelta_prior_to_start_for_active, time_end__gte=now)
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
