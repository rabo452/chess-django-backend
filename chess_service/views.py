# views.py
import json

from django.contrib.auth.models import User
from django.core.exceptions import BadRequest, ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GameRoom, ChessGame
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGameRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:
            name = request.data['name']
        except KeyError:
            raise BadRequest

        try:
            GameRoom.objects.get(player_init=request.user)
            return Response({
                "code": 400,
                "message": "you cannot create a new game room until the old one is finished"
            })
        except ObjectDoesNotExist:
            game_room = GameRoom.objects.create(player_init=request.user, name=name)
            return Response({
                "code": 201,
                "id": game_room.id
            })


class DoesGameRoomExist(APIView):
    def get(self, request: Request):
        try:
            roomId = int(request.query_params.get("roomId"))
        except:
            return Response({
                "code": 400
            })

        try:
            GameRoom.objects.get(id=roomId)
            return Response({
                "code": 200,
                "exist": True
            })
        except ObjectDoesNotExist:
            return Response({
                "code": 200,
                "exist": False
            })


class GetGameRooms(APIView):
    def get(self, request):
        rooms = GameRoom.objects.all()
        result = []

        for room in rooms:
            result.append({
                "id": room.id,
                "name": room.name,
                "player": room.player_init.username
            })

        return Response(json.dumps(result))


class GetUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        try:
            return Response({
                "username": request.user.username
            })
        except:
            return BadRequest()

