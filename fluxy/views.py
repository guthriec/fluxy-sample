from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse

import mailchimp
# mailchimp example app: https://github.com/mailchimp/mcapi2-python-examples


def index(request):
  return render(request, 'fluxy/index.html')

def success(request):
  return render(request, 'fluxy/index.html', {
    'success': True,
  })

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
  return redirect(reverse('fluxy.views.success'))

