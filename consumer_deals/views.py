from django.shortcuts import render

def deals(request):
  return render(request, 'consumer_deals/deals.html', {
                  'title': 'Fluxy Deals',
                  'page_title': 'Deals'
                })
