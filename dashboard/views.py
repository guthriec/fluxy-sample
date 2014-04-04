from django.shortcuts import render

def dashboard(request):
  return render(request, 'dashboard/dashboard.html', {
                 'title': 'Fluxy Dashboard',
                 'page_title': 'Dashboard'
               })
