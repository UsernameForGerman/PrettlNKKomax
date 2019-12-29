# Experiment/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import komax_app.routing
from django.conf.urls import url

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            komax_app.routing.websocket_urlpatterns
        )
    ),
})
