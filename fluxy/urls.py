from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from fluxy import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Registration/authentication
  url(r'^user/auth/$', views.user_auth),
  url(r'^user/register/$', views.user_register),
  url(r'^user/logout/$', views.user_logout),

  # User model
  url(r'^api/v1/user/$', views.user),
  url(r'^api/v1/user/vendors/$', views.user_vendors),
  url(r'^api/v1/user/claimed_deals/$', views.user_deals),
  url(r'^api/v1/user/claimed_deals/all/$', views.user_deals, {'active_only':
                                                              False}),

  # Route landing page resources: /, /success, /subscribe
  url(r'^$', views.index),
  url(r'^subscribe/$', views.subscribe),
  url(r'^success/$', views.success),

  # Route /admin resources
  url(r'^admin/', include(admin.site.urls)),

  url(r'', include('deals.urls')),
  url(r'', include('dashboard.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
