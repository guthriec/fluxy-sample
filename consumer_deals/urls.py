from django.conf.urls import patterns, include, url
from consumer_deals import views

urlpatterns = patterns('',
  # Route deals page
  url(r'^deals/$', views.deals),
)
