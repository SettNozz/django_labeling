from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^loaders/(?P<class_name>[^/]+)/$', views.loaders, name='loaders')
]