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
  # Route /deals/ and /vendors/ resources
  url(r'^deals/$', 'deals.views.deal'),
  url(r'^vendors/$', 'deals.views.vendor'),
  url(r'^deals/(?P<deal_id>\d+)/$', 'deals.views.deal'),
  url(r'^vendors/(?P<vendor_id>\d+)/$', 'deals.views.vendor'),
)
