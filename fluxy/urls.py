from django.conf.urls import patterns, include, url

from fluxy import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Registration/authentication
  url(r'^user/auth/$', views.user_auth),
  url(r'^user/register/$', views.user_register),
  url(r'^user/logout/$', views.user_logout),

  # User model
  url(r'^api/v1/user/vendors/$', views.user_vendors),
  url(r'^api/v1/user/claim/$', views.user_claim),
  url(r'^api/v1/user/claimed-deals/$', views.user_deals),
  url(r'^api/v1/user/claimed-deals/all/$', views.user_deals_all),

  # Route landing page resources: /, /success, /subscribe
  url(r'^$', views.index),
  url(r'^subscribe/$', views.subscribe),
  url(r'^success/$', views.success),

  # Route /admin resources
  url(r'^admin/', include(admin.site.urls)),

  # Deals resources (includes dashboard)
  url(r'^', include('deals.urls', namespace='deals')),
)
