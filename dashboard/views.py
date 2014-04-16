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
    messages.add_message(request, messages.ERROR, "You don't own any restaurants!")
    return redirect(reverse('fluxy.views.login_page'))
