import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import myhome.routing as routing
from myhome.routing import websocket_urlpatterns
from chanmqttproxy import MqttConsumer


application =   ProtocolTypeRouter(
    {
        "channel": ChannelNameRouter({"mqtt": MqttConsumer.as_asgi()}),
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    },
)
