
import os
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chatAplicativo.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "giro_dance.settings")

django_asgi_app = get_asgi_application()

django_asgi_app = ASGIStaticFilesHandler(django_asgi_app)

application = ProtocolTypeRouter({
    "http": django_asgi_app,  
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatAplicativo.routing.websocket_urlpatterns
        )
    ),
})
