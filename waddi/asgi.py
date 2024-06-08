"""
ASGI config for waddi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from orders.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from orders.middlewares import TokenAuthMiddleWare

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "waddi.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleWare(
            URLRouter(websocket_urlpatterns),
        ),
    }
)
