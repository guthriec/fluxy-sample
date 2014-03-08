from django.conf.urls import patterns, include, url

from deals import views

urlpatterns = patterns('',
  url(r'^dashboard$', views.dashboard),
)
