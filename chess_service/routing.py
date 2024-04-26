# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chess/game-room/(?P<room_id>\w+)/$", consumers.ChessRoomConsumer.as_asgi()),
    re_path(r"ws/chess/game/(?P<game_id>\w+)/$", consumers.ChessGameConsumer.as_asgi())
]