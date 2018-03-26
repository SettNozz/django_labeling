from django.conf.urls import url

from . import consumer

websocket_urlpatterns = [
    url(r'^ws/myapp/loaders/(?P<class_name>[^/]+)/$', consumer.ChatConsumer),
]
