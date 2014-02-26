from django.shortcuts import render
from django.http import HttpResponse

import mailchimp


def index(request):
  return render(request, 'fluxy/index.html')

def subscribe(request):
  try:
    m = mailchimp.Mailchimp('f8dd77b845c2045f7df529b04427bd98-us3')
    m.lists.subscribe('56437bae31', {'email':request.POST['email']},
        double_optin=False)
  except mailchimp.ListAlreadySubscribedError:
    return HttpResponse("You've already subscribed. Thanks though!")
    # return render(request, 'fluxy/index.html')
  except mailchimp.Error, e:
    return HttpResponse("An error occured %s: %s" % (e.__class__, e))
  return HttpResponse("You're good")
