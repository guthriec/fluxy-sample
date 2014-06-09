from django.conf.urls import patterns, url
from landing_page import views

urlpatterns = patterns('',
  url(r'^$', views.index),
)
