from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/post/(?P<pk>\w+)/$", consumers.PostConsumer.as_asgi()),
]