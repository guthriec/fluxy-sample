from django.conf.urls import patterns, include, url

from deals import views

urlpatterns = patterns('',
  url(r'^dashboard/$', views.dashboard),

  # Route API
  url(r'^api/v1/deals/$', views.deal),
  url(r'^api/v1/vendors/$', views.vendor),
  url(r'^api/v1/deals/(?P<deal_id>\d+)/$', 'deals.views.deal'),
  url(r'^api/v1/vendors/(?P<vendor_id>\d+)/$', 'deals.views.vendor'),
  url(r'^api/v1/vendors/(?P<vendor_id>\d+)/deals/$', 'deals.views.vendor_deals'),
  url(r'^api/mock/deals/$', 'deals.views.mock_deal'),
  url(r'^api/mock/vendors/$', 'deals.views.mock_vendor'),
  url(r'^api/mock/vendors/(?P<vendor_id>\d+)/$', 'deals.views.mock_vendor'),
  url(r'^api/mock/deals/(?P<deal_id>\d+)/$', 'deals.views.mock_deal'),
)
