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
    return redirect(reverse('fluxy.views.login_page'))
