from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

@login_required
def dashboard(request):
  try: 
    return render(request, 'dashboard/dashboard.html', {
                   'title': 'Fluxy Dashboard',
                   'page_title': 'Dashboard',
                   'vendor_id': request.session['vendor_id']
                 })
  except KeyError:
    messages.add_message(request, messages.ERROR, "The credentials you provided aren't associated with any restaurants. Login with different credentials to access the restaurant dashboard, or download our mobile app to view and claim deals!")
    return redirect(reverse('fluxy.views.login_page'))
