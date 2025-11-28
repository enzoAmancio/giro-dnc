"""
ASGI config for giro_dance project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import calendario.routing  # ajuste para o app correto

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giro_dance.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            calendario.routing.websocket_urlpatterns
        )
    ),
})