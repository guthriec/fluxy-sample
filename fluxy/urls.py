from django.conf.urls import patterns, include, url

from fluxy import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Route landing page resources: /, /success, /subscribe
  url(r'^$', views.index),
  url(r'^subscribe$', views.subscribe),
  url(r'^success$', views.success),

  # Route /admin resources
  url(r'^admin/', include(admin.site.urls)),

  # Route API
  url(r'^api/v1/deals/$', 'deals.views.deal'),
  url(r'^api/v1/deals/(?P<deal_id>\d+)/$', 'deals.views.deal'),

  url(r'^api/v1/vendors/$', 'deals.views.vendor'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/$', 'deals.views.vendor'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/deals/$',
    'deals.views.vendor_deals'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/deals/(?P<deal_id>\d+)/$',
    'deals.views.vendor_deals'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/deals/all/$',
    'deals.views.vendor_deals_all'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/claimed_deals/$',
    'deals.views.vendor_claimed_deals'),
  url(r'^api/v1/vendor/(?P<vendor_id>\d+)/claimed_deals/all/$',
    'deals.views.vendor_claimed_deals_all', {'active': False}),

  url(r'^api/mock/vendors/$', 'deals.views.mock_vendor'),
  url(r'^api/mock/vendors/(?P<vendor_id>\d+)/$', 'deals.views.mock_vendor'),
  url(r'^api/mock/deals/(?P<deal_id>\d+)/$', 'deals.views.mock_deal'),
)
