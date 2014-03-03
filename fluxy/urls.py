from django.conf.urls import patterns, include, url

from fluxy import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Registration/authentication
  url(r'^api/v1/auth/$', views.vendor_auth),
  url(r'^api/v1/register/$', views.vendor_reg),
  
  # Route landing page resources: /, /success, /subscribe
  url(r'^$', views.index),
  url(r'^subscribe/$', views.subscribe),
  url(r'^success/$', views.success),

  # Route /admin resources
  url(r'^admin/', include(admin.site.urls)),

  # Deals resources (includes dashboard)
  url(r'^', include('deals.urls', namespace='deals')),
)
