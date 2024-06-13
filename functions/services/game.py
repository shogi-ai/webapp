from firebase_functions.https_fn import FunctionsErrorCode, HttpsError

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

    def make_move(self, uid: str, from_square: str, to_square: str):
        game = self.game_repository.get(uid)
        if game is None:
            raise HttpsError(
                code=FunctionsErrorCode.NOT_FOUND,
                message="Invalid game id",
            )

        for move in game["moves"]:
            self.shogi_board.make_move(move["from_square"], move["to_square"])

        self.shogi_board.make_move(from_square, to_square)

        game["moves"].append({"from_square": from_square, "to_square": to_square})
        bitboard, pieces_in_hand = self.shogi_board.get_board()
        game.board = bitboard
        game.pieces_in_hand = pieces_in_hand
        self.game_repository.update(game)

    def get_legal_moves(self, uid: str, from_square: str):
        game = self.game_repository.get(uid)
        if game is None:
            raise HttpsError(
                code=FunctionsErrorCode.NOT_FOUND,
                message="Invalid game id",
            )

        for move in game["moves"]:
            self.shogi_board.make_move(move["from_square"], move["to_square"])

        return self.shogi_board.get_legal_moves(from_square)
