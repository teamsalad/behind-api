from channels.routing import ProtocolTypeRouter, URLRouter
from behind.authentication import TokenAuthMiddlewareStack

import chats.routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    ),
})
