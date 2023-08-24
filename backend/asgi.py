"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# isort: skip_file
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from recipe.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator
from recipe.token_auth import JwtAuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":AllowedHostsOriginValidator(
        JwtAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
    ) ,
})

