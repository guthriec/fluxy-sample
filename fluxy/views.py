# Filename: /fluxy/views.py
# Notes: Includes view functions for the overall Fluxy project

from deals.api_tools import make_post_response
from deals.models import Deal, ClaimedDeal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.timezone import utc
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from fluxy.models import FluxyUser
import datetime
import json
import mailchimp
# mailchimp example app: https://github.com/mailchimp/mcapi2-python-examples

def index(request):
  """
  Author: Rahul Gupta-Iwasaki
  Path: /
  Description: Renders the landing page
  """
  return render(request, 'fluxy/index.html', {'title': 'Fluxy'})

def success(request):
  """
  Author: Rahul Gupta-Iwasaki
  Path: /success
  Description: Renders the landing page with a success message
  """
  return render(request, 'fluxy/index.html', {
    'title': 'Fluxy',
    'success': True,
  })

def subscribe(request):
  """
  Author: Rahul Gupta-Iwasaki
  Path: /subscribe
  Description: Takes post with email parameter, synchronously posts this to
  Mailchimp trying to subscribe the email. Either returns an error message or
  redirects the client to /success displaying a success message
  """
  try:
    m = mailchimp.Mailchimp('f8dd77b845c2045f7df529b04427bd98-us3')
    m.lists.subscribe('56437bae31', {'email':request.POST['email']},
        double_optin=False)
  except mailchimp.ListAlreadySubscribedError:
    return render(request, 'fluxy/index.html', {
      'error_message': "You've already subscribed for updates. Thanks though!",
    })
  except mailchimp.Error, e:
    return render(request, 'fluxy/index.html', {
      # We could display the specific error that occurs using e, but
      # that doesn't seem very user friendly
      'error_message': "Oh no! An error occured! Try again?",
    })
  except:
    return render(request, 'fluxy/index.html')
  return redirect(reverse('fluxy.views.success'))

def register_page(request):
  """
  @author: Chris
  @desc: renders registration page, handles posts from this page.
  If user is authenticated, redirects to dashboard.
  """
  error_message = None
  for message in messages.get_messages(request):
    if message.level == messages.ERROR:
      error_message = message.message

  if request.method == 'POST':
    api_resp = user_register(request)
    api_content = None
    if api_resp.status_code != 201:
      api_content = json.loads(api_resp.content)
      error_message = api_content['message']
      messages.add_message(request, messages.ERROR, error_message)
    else:
      return redirect(reverse('fluxy.views.login_page'))

  return render(request, 'fluxy/register.html', {
                 'title': 'Fluxy Registration',
                 'error_message': error_message,
                 'page_title': 'Register'
               })

def login_page(request):
  """
  @author: Chris
  @desc: renders login page, handles auth posts from the login page.
  If user is authenticated, redirects to dashboard.
  Right now, ignores the 'next' parameter. If the user has associated
  vendors, it redirects to the dashboard for the first vendor in the list.
  """
  error_message = None
  for message in messages.get_messages(request):
    if message.level == messages.ERROR:
      error_message = message.message

  if request.method == 'POST':
    api_resp = user_auth(request)
    api_content = json.loads(api_resp.content)
    if api_resp.status_code != 200 or not api_content['success']:
      error_message = api_content['message']
    else:
      try:
        vendor_id = api_content['response']['vendors'][0]
        request.session['vendor_id'] = vendor_id
      # If no associated vendor, just don't set the vendor_id session attribute
      except IndexError:
        pass
      return redirect(reverse('dashboard.views.dashboard'))

  return render(request, 'fluxy/login.html', {
                 'title': 'Fluxy Login',
                 'error_message': error_message,
                 'page_title': 'Login'
               })

def logout_page(request):
  """
  @author: Chris
  @desc: handles logout requests from the /logout/ URL, redirecting
  to an appropriate webpage
  """
  if request.user.is_authenticated():
    user_logout(request)
  return redirect(reverse('fluxy.views.login_page'))

def _login_user_and_respond(request, fluxy_user):
  response = {}
  if fluxy_user is not None:
    login(request, fluxy_user)
    response = {
      "code": 200,
      "message": "Authentication successful",
      "success": True,
      "response": fluxy_user.get_safe_user()
    }
  else:
    response = {
      "code": 401,
      "message": "Authentication failed - try a different username/password or user Facebook login",
      "success": False
    }
    return HttpResponse(json.dumps(response), content_type="application/json", status = response['code'])

@csrf_exempt
@require_http_methods(["POST"])
def user_auth(request):
  """
  @author: Chris, Rahul, Ayush
  @desc: This method is used to log a user in. Returns a 200 upon a valid
  request, 401 on invalid login credientials and a 400 on a badly formated
  request. Accepts either standard form or JSON formatted POSTs with the
  following keys:
      *email
      *password

  @param request: the request object

  @return: 200 on valid request, 400 otherwise. Valid post's reponse is JSON
  with key "success" indicating the success of the login.
  """
  post_data = request.POST
  username = None
  password = None
  access_token = None
  if request.META['CONTENT_TYPE'] == 'application/json':
    post_data = json.loads(request.body)
  if 'username' in post_data and 'password' in post_data:
    username = post_data['email'].lower()
    password = post_data['password']
  elif 'access_token' in post_data:
    access_token = post_data['access_token']
  else:
    response = { 'code': 400, 'success': False, 'message': 'Request must include either username/password or a Facebook access token.' }
    return HttpResponse(json.dumps(response), status = 400,
        content_type='application/json')

  user = authenticate(username=username, password=password, access_token=access_token)
  return _login_user_and_respond(user)

@csrf_exempt
@require_http_methods(["POST"])
def user_register(request):
  """
  @author: Chris, Rahul
  @desc: This method registers a new user. Returns 200 upon success, 400
  otherwise. It does not log the user in upon successful registration.
  Accepts either standard form or JSON formatted POSTs with the following keys:
      *email
      *password
      *password_confirm

  @param request: the request object

  @return: 201 on successful registration, 400 otherwise
  """
  post_data = request.POST
  try:
    if request.META['CONTENT_TYPE'] == 'application/json':
      post_data = json.loads(request.body)
    email = post_data['email'].lower()
    username = post_data['email'].lower()
    password = post_data['password']
    password_confirm = post_data['password_confirm']
  except Exception:
    return make_post_response(None, None, {'code': 400, 'message': 'Missing fields or malformed request.'})
  known_error = {'code': 400, 'message': 'Could not register'}
  if password != password_confirm:
    known_error['message'] = "Passwords do not match"
  else:
    try:
      FluxyUser.objects.get(username__exact=username)
      known_error['message'] = "Username already registered"
    except FluxyUser.DoesNotExist:
      new_user = FluxyUser.objects.create_user(email=email, username=username, password=password, fb_only=False)
      new_user.save()
      logged_in_user = authenticate(username=username, password=password)
      login(request, logged_in_user)
      user_list = [logged_in_user.get_safe_user()]
      return make_post_response(user_list, '/user/')
  return make_post_response(None, None, known_error)

@require_http_methods(["GET"])
def user_logout(request):
  """
  @author: Rahul
  @desc: This method logs any authenticated user out.

  @param request: the request object

  @return: 200 on success, 302 redirect to /user/auth/ otherwise
  """
  if not request.user.is_authenticated():
    return redirect('/user/auth/')
  else:
    logout(request)
    response = {"code": 200, "message": "Logged out."}
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = response['code'])

@require_http_methods(["GET"])
def user(request):
  """
  @author: Rahul
  @desc: This method returns a JSON object containing the currently
  authenticated user's details.

  @param request: the request object

  @return: A JSON encoded subset of the user object if there is a logged in
  user, otherwise a 401 error
  """
  if not request.user.is_authenticated():
    response = {'code': 401, 'message': 'Authentication error'}
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = response['code'])
  else:
    return HttpResponse(json.dumps([request.user.get_safe_user()]),
                        content_type="application/json")

@require_http_methods(["GET"])
def user_vendors(request):
  """
  Author: Rahul Gupta-Iwasaki
  This method returns a JSON array of all the vendors which the user has
  administrative power over.
  """
  if not request.user.is_authenticated():
    response = {'code': 401, 'message': 'Authentication error'}
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = response['code'])
  else:
    return HttpResponse(serializers.serialize('json', request.user.vendors.all()),
                        content_type="application/json")

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def user_deals(request, active_only=True):
  """
  @author: Rahul Gupta-Iwasaki
  @desc: If GET, this returns a JSON array contain the user's deals. Depending
  on the active_only param, will return only active deals or all deals.

  If POST, create a new claimed deal. Use the following keys:
      *deal_id
      *latitude OPTIONAL
      *longitude OPTIONAL

  @param request: the request object
  @param active_only: specifies whether to include expired deals or not in the
  response. Only relevant to GET.

  @returns: a JSON encoded array of deals the user has claimed
  """
  if not request.user.is_authenticated():
    response = {'code': 401, 'message': 'Authentication error'}
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = response['code'])
  now = datetime.datetime.utcnow().replace(tzinfo=utc)
  if request.method == 'POST':
    post_data = request.POST
    try:
      if request.META['CONTENT_TYPE'] == 'application/json':
        post_data = json.loads(request.body)
      deal = Deal.objects.get(pk=post_data['deal_id'], time_start__lte=now,
                              time_end__gte=now)
      latitude = post_data.get('latitude', None)
      longitude = post_data.get('longitude', None)
      claimed_deal = ClaimedDeal.objects.create(user=request.user, deal=deal,
          claimed_latitude=latitude, claimed_longitude=longitude)
      claimed_deal.save()
      return HttpResponseRedirect('/api/v1/users/claimed_deal/',
                  serializers.serialize('json', [claimed_deal]),
                  content_type='application/json', status=201)
    except Exception:
      pass
    return HttpResponse("Bad request.", status=400)
  else:
    claimed_deals = request.user.claimeddeal_set.all()
    if active_only:
      claimed_deals = claimed_deals.filter(deal__time_end__gte=now,
                                           deal__time_start__lte=now)
    return HttpResponse(serializers.serialize('json', claimed_deals),
                        content_type="application/json")


