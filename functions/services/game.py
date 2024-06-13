from repository.dataclasses.game import Game
from repository.game_repository import GameReposiory
from services.board import ShogiBoard


class GameService:
    def __init__(self, app: any, shogi_board: ShogiBoard):
        self.app: any = app
        self.shogi_board: ShogiBoard = shogi_board
        self.game_repository: GameReposiory = GameReposiory(self.app)

    def create(self) -> str:
        bitboard, pieces_in_hand = self.shogi_board.get_board()
        game = Game(moves=[], board=bitboard, pieces_in_hand=pieces_in_hand)
        self.game_repository.create(game)
        return game.uid
