from django.conf.urls import patterns, include, url

from fluxy import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', views.index),
  url(r'^subscribe$', views.subscribe),
  url(r'^success$', views.success),
  url(r'^dashboard$', 'deals.views.dashboard'),
  url(r'^admin/', include(admin.site.urls)),
  # Route /deals/ and /vendors/ resources
  url(r'^/api/v1/deals$', 'deals.views.deal'),
  url(r'^/api/v1/vendors$', 'deals.views.vendor'),
  url(r'^/api/v1/deals/(?P<deal_id>\d+)/$', 'deals.views.deal'),
  url(r'^/api/v1/vendors/(?P<vendor_id>\d+)/$', 'deals.views.vendor'),
)
