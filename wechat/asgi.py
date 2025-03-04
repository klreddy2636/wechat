"""
ASGI config for wechat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from chat import consumers
from chat.middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechat.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': JWTAuthMiddleware(
        URLRouter([
            path('ws/socket-server/', consumers.MyConsumer.as_asgi()),  # Connect to video consumer
        ])
    )
})
