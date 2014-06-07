from django.shortcuts import render

# Create your views here.
def index(request):
  """
  Author: Rahul Gupta-Iwasaki
  Path: /
  Description: Renders the landing page
  """
  return render(request, 'index.html', {'title': 'Fluxy'})
