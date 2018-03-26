from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from myapp.consumer import ThumbnailConsumer
import myapp.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            myapp.routing.websocket_urlpatterns
        )
    ),
    "channel": ChannelNameRouter({
            "thumbnails-generate": ThumbnailConsumer
        }),
})

