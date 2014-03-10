# Filename: /fluxy/views.py
# Notes: Includes view functions for the overall Fluxy project

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
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

@require_http_methods(["POST"])
def user_auth(request):
  """
  Author: Chris Guthrie
  This method is used to log a user in.
  """
  post_data = json.loads(request.body)
  username = post_data['username']
  password = post_data['password']
  user = authenticate(username=username, password=password)
  response = {}
  if user is not None:
    login(request, user)
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = 200)
  else:
    response = {"code": 401, "message": "Invalid username/password", "success": False}
    return HttpResponse(json.dumps(response), content_type="application/json", status = response["code"])

@require_http_methods(["POST"])
def user_register(request):
  """
  Author: Chris Guthrie
  This method registers a new user.
  """
  post_data = json.loads(request.body)
  username = post_data['username']
  password = post_data['password']
  response = {"code": 401, "message": "Could not register"}
  try:
    FluxyUser.objects.get(username__exact=username)
    response['message'] = "Username already registered"
  except FluxyUser.DoesNotExist:
    new_user = FluxyUser.objects.create_user(username=username, password=password)
    new_user.user_permissions.add(Permission.objects.get(codename='change_deal'))
    new_user.save()
    response = {"code": 200, "message": "Successfully registered"}
  return HttpResponse(json.dumps(response), content_type="application/json",
                      status = response['code'])

@require_http_methods(["GET"])
def user_logout(request):
  """
  Author: Rahul Gupta-Iwasaki
  This method logs any authenticated user out.
  """
  logout(request)
  response = {"code": 200, "message": "Logged out."}
  return HttpResponse(json.dumps(response), content_type="application/json",
                      status = response['code'])

@require_http_methods(["GET"])
def user(request):
  """
  Author: Rahul Gupta-Iwasaki
  This method returns a JSON object contianing the currently authenticated
  user's details.
  """
  if not request.user.is_authenticated():
    response = {'code': 403, 'message': 'Authentication error'}
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = response['code'])
  else:
    return HttpResponse(json.dumps(request.user),
                        content_type="application/json")

@require_http_methods(["GET"])
def user_vendors(request):
  """
  Author: Rahul Gupta-Iwasaki
  This method returns a JSON array of all the vendors which the user has
  administrative power over.
  """
  if not request.user.is_authenticated():
    response = {'code': 403, 'message': 'Authentication error'}
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = response['code'])
  else:
    return HttpResponse(json.dumps(response.user.vendors.all()),
                        content_type="application/json")

@require_http_methods(['GET', 'POST'])
def user_deals(request):
  """
  Author: Rahul Gupta-Iwasaki
  If GET, this returns a JSON array contain the user's ACTIVE deals.

  Note, when making this query on my local machine, it was throwing a
  RuntimeError complaining about the time_end field receiving a naive datetime
  while time zone support is active. This was remedied by turning the USE_TZ
  setting off in settings.py. However, it seems we would rather have this on,
  and the problem is the sqlite db doesn't support time zones. If so, this
  should go away in production, but we should verify this.

  If POST, create a new claimed deal.
  """
  if not request.user.is_authenticated():
    response = {'code': 403, 'message': 'Authentication error'}
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = response['code'])
  if request.method == 'POST':
    post_data = json.loads(request.body)
    deal = post_data['deal_id']
    latitude = post_data['latitude']
    longitude = post_data['longitude']
    claimed_deal = ClaimedDeal.objects.create(deal=deal,
                      claimed_latitude=latitude, claimed_longitude=longitude)
    claimed_deal.save()
    return HttpResponse('Successfully claimed deal.',
                        content_type='application/json')
  else:
    return HttpResponse(json.dumps(response.user.claimeddeal_set.filter(
                              deal__time_end__lte=datetime.datetime.now())),
                              content_type="application/json")

@require_http_methods(["GET"])
def user_deals_all(request):
  """
  Author: Rahul Gupta-Iwasaki
  This returns a JSON array contain all the currently authenticated user's
  deals, including those that have expired or been completed.
  """
  if not request.user.is_authenticated():
    response = {'code': 403, 'message': 'Authentication error'}
    return HttpResponse(json.dumps(response), content_type="application/json",
                        status = response['code'])
  else:
    return HttpResponse(json.dumps(response.user.claimeddeal_set.all()),
                        content_type="application/json")

