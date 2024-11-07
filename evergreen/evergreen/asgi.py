"""
ASGI config for evergreen project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evergreen.settings")

# this is for websockets
application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    # TODO: add websocket config here, after wards
})

application = get_asgi_application()