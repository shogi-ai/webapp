"""Service to manage the game state"""

from firebase_functions.https_fn import FunctionsErrorCode, HttpsError

from repository.dataclasses.game import Game
from repository.game_repository import GameRepository
from services.board import ShogiBoard
from services.agent import ShogiAgent


class GameService:
    """Service to manage the game state"""

    def __init__(self, app: any):
        self.app: any = app
        self.shogi_board = ShogiBoard()
        self.game_repository = GameRepository(self.app)
        self.shogi_agent = ShogiAgent("/tmp/shogi-agent.pth")

    def create(self) -> str:
        """Initialize new game"""
        bitboard, pieces_in_hand = self.shogi_board.get_board()
        game = Game(moves=[], board=bitboard, pieces_in_hand=pieces_in_hand)
        self.game_repository.create(game)
        return game.uid

    def make_move(self, uid: str, from_square: str, to_square: str, promotion: bool):
        """Add a new move to the game"""
        # Get game, and the board
        game = self._get_game(uid)

        # Make new move
        self.shogi_board.make_move(from_square, to_square, promotion)

        # Update game object
        game.moves.append(
            {"from_square": from_square, "to_square": to_square, "promotion": promotion}
        )
        game.board, game.pieces_in_hand = self.shogi_board.get_board()
        self.game_repository.update(game)

    def get_legal_moves(self, uid: str, from_square: str):
        """Get all legal moves for the specified fame, and piece"""
        # Get game, and the board
        _ = self._get_game(uid)
        # Get the legal moves
        return self.shogi_board.get_legal_moves(from_square)

    def _get_game(self, uid: str) -> Game:
        """Get the selected game and update the board accordingly"""
        game = self.game_repository.get(uid)
        if game is None:
            raise HttpsError(
                code=FunctionsErrorCode.NOT_FOUND,
                message="Invalid game id",
            )

        for move in game.moves:
            self.shogi_board.make_move(
                move["from_square"], move["to_square"], move["promotion"]
            )
        return game


    def get_best_move(self, uid: str):
        """Get the best move for the current player"""
        _ = self._get_game(uid)
        move, move_index = self.shogi_agent.select_best_action(self.shogi_board)
        return move, move_index