"""
Welcome to Cloud Functions for Firebase for Python!
To get started, simply uncomment the below code or create your own.
Deploy with `firebase deploy
"""

from firebase_functions.https_fn import on_call, CallableRequest, HttpsError, FunctionsErrorCode
from firebase_functions import options
from firebase_admin import initialize_app
from services.board import ShogiBoard
from services.game import GameService

app = initialize_app()
options.set_global_options(region=options.SupportedRegion.EUROPE_WEST1)

shogi_board = ShogiBoard()
game_manager = GameService(app, shogi_board)


@on_call(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def create_game(_: CallableRequest):
     data = game_manager.create()
     return data


@on_call(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def read_board(_: CallableRequest):
    data = {
        "board": shogi_board.get_board()
    }
    return data

@on_call(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def make_move(req: CallableRequest):
    move_str = req.data.get("move")
    if move_str is None:
        raise HttpsError(
            code=FunctionsErrorCode.NOT_FOUND,
            message="Invalid from_square",
        )
    data = {
        "board": shogi_board.make_move(move_str)
    }
    return data

@on_call(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def read_legal_moves(req: CallableRequest):
    piece_from_square = req.data.get("from_square")
    if piece_from_square is None:
        raise HttpsError(
            code=FunctionsErrorCode.NOT_FOUND,
            message="Invalid from_square",
        )

    data = {
        "legal_moves": shogi_board.get_legal_moves(piece_from_square)
    }

    return data