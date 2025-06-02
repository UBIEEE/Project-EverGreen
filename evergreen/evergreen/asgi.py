"""
ASGI config for evergreen project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# CAUTION: Do not put any custom imports until after the application has been gotten
# with django_asgi_app = get_asgi_application()
# source:
# https://channels.readthedocs.io/en/latest/deploying.html#configuring-the-asgi-application
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evergreen.settings")
django_asgi_app = get_asgi_application()

# Define your custom imports from here...
from eg_app.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
