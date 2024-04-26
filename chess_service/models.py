from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ChessGame(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_white')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_black')
    board = models.CharField(max_length=1000, null=False,
                             default="""[[{"figureNumber":10,"turnsMade":0},{"figureNumber":9},{"figureNumber":8},{"figureNumber":11},{"figureNumber":12,"turnsMade":0},{"figureNumber":8},{"figureNumber":9},{"figureNumber":10,"turnsMade":0}],[{"figureNumber":7,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":7,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":7,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":7,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":7,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":7,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":7,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":7,"turnsMade":0,"canBeBeatenAsideWithinTurn":0}],[{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0}],[{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0}],[{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0}],[{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0},{"figureNumber":0}],[{"figureNumber":1,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":1,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":1,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":1,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":1,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":1,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":1,"turnsMade":0,"canBeBeatenAsideWithinTurn":0},{"figureNumber":1,"turnsMade":0,"canBeBeatenAsideWithinTurn":0}],[{"figureNumber":4,"turnsMade":0},{"figureNumber":3},{"figureNumber":2},{"figureNumber":5},{"figureNumber":6,"turnsMade":0},{"figureNumber":2},{"figureNumber":3},{"figureNumber":4,"turnsMade":0}]]""")
    playerTurn = models.CharField(max_length=30, default="player_white")
    turnCount = models.IntegerField(default=1)
    turnSecondsIncrease = models.IntegerField(default=2)
    player1SecondsTime = models.IntegerField(default=40 * 60)
    player2SecondsTime = models.IntegerField(default=40 * 60)
    isGameOver = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    lastUpdated = models.DateTimeField(auto_now=True)

    async def get_player1(self):
        return await self.player1

    async def get_player2(self):
        return await self.player2



class GameRoom(models.Model):
    name = models.CharField(max_length=255, null=False)
    player_init = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_init')