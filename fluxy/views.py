# Filename: /fluxy/views.py
# Notes: Includes view functions for the overall Fluxy project

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

import mailchimp
# mailchimp example app: https://github.com/mailchimp/mcapi2-python-examples

"""
  Author: Rahul Gupta-Iwasaki
  Path: /
  Description: Renders the landing page
"""
def index(request):
  return render(request, 'fluxy/index.html', {'title': 'Fluxy'})

"""
  Author: Rahul Gupta-Iwasaki
  Path: /success
  Description: Renders the landing page with a success message
"""
def success(request):
  return render(request, 'fluxy/index.html', {
    'title': 'Fluxy',
    'success': True,
  })

"""
  Author: Rahul Gupta-Iwasaki
  Path: /subscribe
  Description: Takes post with email parameter, synchronously posts this to
  Mailchimp trying to subscribe the email. Either returns an error message or
  redirects the client to /success displaying a success message
"""
def subscribe(request):
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

