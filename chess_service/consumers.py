# myapp/consumers.py
import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from chess_service.models import GameRoom, ChessGame
from chess_service.services.AuthService import is_access_token_valid, get_user_id


class ChessRoomConsumer(AsyncWebsocketConsumer):
    users = set()

    async def connect(self):
        try:
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        except KeyError:
            await self.close(400)

        try:
            await sync_to_async(GameRoom.objects.get)(id=int(self.room_id))
        except ObjectDoesNotExist:
            await self.close(400)

        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        room = await sync_to_async(GameRoom.objects.get)(id=int(self.room_id))
        await sync_to_async(room.delete)()

        self.channel_layer.group_send(
            self.room_id,
            {
                type: "group.destroy"
            }
        )

        await self.channel_layer.group_discard(
            self.room_id,
            self.channel_name
        )

    async def receive(self, text_data):
        token = json.loads(text_data)['access']
        if not is_access_token_valid(token):
            return
        user = await sync_to_async(User.objects.get)(id=get_user_id(token))
        self.users.add(user)

        if len(self.users) < 2:
            return

        users = list(self.users)
        game = await sync_to_async(ChessGame.objects.create)(
            player1=users[0],
            player2=users[1]
        )

        await self.channel_layer.group_send(
            self.room_id,
            {
                "type": "group.gameCreated",
                "game": game
            }
        )

    async def group_destroy(self):
        await self.close()

    async def group_gameCreated(self, event):
        await self.send(json.dumps({
            "action": "game-created",
            "game_id": event['game'].id
        }))
        await self.disconnect(200)


class ChessGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        except KeyError:
            await self.close(400)

        try:
            self.game = await sync_to_async(ChessGame.objects.get)(id=self.game_id)
        except:
            await self.close(400)

        await self.channel_layer.group_add(
            self.game_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.game_id,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            token = data['access_token']
            action = data["action"]
        except:
            return

        if not is_access_token_valid(token):
            return

        self.user = await sync_to_async(User.objects.get)(id=get_user_id(token))
        game = self.game

        if (await sync_to_async(lambda: game.player1)()) != self.user and (await database_sync_to_async(lambda: game.player2)()) != self.user:
            await self.disconnect(401)

        if action == "connection":
            await self.connection_action()

        if action == "makeTurn":
            await self.makeTurn_action(data)

    async def connection_action(self):
        game = self.game

        if self.user == game.player1:
            player_team = "white"
        else:
            player_team = "black"

        await self.send(json.dumps({
            "action": "game-info",
            "board": game.board,
            "player_team": player_team,
            "playerTurn": game.playerTurn,
            "turnCount": game.turnCount
        }))

    async def makeTurn_action(self, data):
        try:
            board = data['board']
        except:
            return

        self.game.board = board
        self.game.turnCount = self.game.turnCount + 1
        if self.game.playerTurn == "player_white":
            self.game.playerTurn = "player_black"
        elif self.game.playerTurn == "player_black":
            self.game.playerTurn = "player_white"

        await sync_to_async(self.game.save)()

        await self.channel_layer.group_send(
            self.game_id,
            {
                "type": "group.update",
                "game": self.game,
            }
        )

    async def group_update(self, event):
        game = self.game = event['game']

        if self.user == game.player1:
            player_team = "white"
        else:
            player_team = "black"

        await self.send(json.dumps({
            "action": "game-info",
            "board": game.board,
            "player_team": player_team,
            "playerTurn": game.playerTurn,
            "turnCount": game.turnCount
        }))
