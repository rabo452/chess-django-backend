from django.contrib.auth.models import User

from chess_service.models import ChessGame


class ChessService:
    def create_game(self, player1: User, player2: User,
                    turnSecondsIncrease: int, player1SecondsTime: int, player2SecondsTime: int):
        game = ChessGame(player1=player1, player2=player2, turnSecondsIncrease=turnSecondsIncrease,
                         player1SecondsTime=player1SecondsTime, player2SecondsTime=player2SecondsTime)
        game.save()
        return game.id