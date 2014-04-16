from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from fluxy import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Registration/authentication
  url(r'^api/v1/user/auth/$', views.user_auth),
  url(r'^api/v1/user/register/$', views.user_register),
  url(r'^api/v1/user/logout/$', views.user_logout),

  # User model
  url(r'^api/v1/user/$', views.user),
  url(r'^api/v1/user/vendors/$', views.user_vendors),
  url(r'^api/v1/user/claimed_deals/$', views.user_deals),
  url(r'^api/v1/user/claimed_deals/all/$', views.user_deals, {'active_only':
                                                              False}),
  # Route login
  url(r'^login/$', views.login_page),
  url(r'^logout/$', views.logout_page),
  url(r'^register/$', views.register_page),

  # Route landing page resources: /, /success, /subscribe
  url(r'^$', views.index),
  url(r'^subscribe/$', views.subscribe),
  url(r'^success/$', views.success),

  # Route /admin resources
  url(r'^admin/', include(admin.site.urls)),

  url(r'', include('deals.urls')),
  url(r'', include('dashboard.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
