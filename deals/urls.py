from django.conf.urls import patterns, include, url
from deals import views

urlpatterns = patterns('',
  # Route API
  url(r'^api/v1/deals/$', 'deals.views.deal'),
  url(r'^api/v1/deals/all/$', 'deals.views.deal', { 'active_only': False }),
  url(r'^api/v1/deals/(?P<deal_id>\d+)/$', 'deals.views.deal',
    { 'active_only': False}),

  url(r'^api/v1/vendors/$', 'deals.views.vendor'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/$', 'deals.views.vendor'),

  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/deals/$',
    'deals.views.vendor_deals'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/deals/all/$',
    'deals.views.vendor_deals', { 'active_only': False }),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/deal/(?P<deal_id>\d+)/$',
    'deals.views.vendor_deals'),

  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/claimed_deals/$',
    'deals.views.vendor_claimed_deals'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/claimed_deals/all/$',
    'deals.views.vendor_claimed_deals', { 'active_only': False }),
)
