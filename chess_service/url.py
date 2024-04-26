from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from chess_service.views import UserCreateAPIView, CreateGameRoom, GetGameRooms, DoesGameRoomExist, GetUser

urlpatterns = [
    path('api/user-create', UserCreateAPIView.as_view(), name='user-create'),
    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/chess/create-game-room", CreateGameRoom.as_view(), name="create_game_room"),
    path("api/chess/get-rooms", GetGameRooms.as_view(), name="get-rooms"),
    path("api/chess/does-room-exist", DoesGameRoomExist.as_view(), name="room-exist"),
    path("api/get-user", GetUser.as_view(), name="get-user")
]