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
def make_move(req: CallableRequest):
    from_square = req.data.get("from_square")
    to_square = req.data.get("to_square")
    uid = req.data.get("uid")

    if from_square is None:
        raise HttpsError(
            code=FunctionsErrorCode.FAILED_PRECONDITION,
            message="Invalid from_square",
        )
    if to_square is None:
        raise HttpsError(
            code=FunctionsErrorCode.FAILED_PRECONDITION,
            message="Invalid from_square",
        )
    if uid is None:
        raise HttpsError(
            code=FunctionsErrorCode.FAILED_PRECONDITION,
            message="Invalid from_square",
        )

    return game_manager.make_move(uid,  from_square, to_square)

@on_call(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def read_legal_moves(req: CallableRequest):
    from_square = req.data.get("from_square")
    uid = req.data.get("uid")

    if from_square is None:
        raise HttpsError(
            code=FunctionsErrorCode.FAILED_PRECONDITION,
            message="Invalid from_square",
        )
    if uid is None:
        raise HttpsError(
            code=FunctionsErrorCode.FAILED_PRECONDITION,
            message="Invalid from_square",
        )

    return game_manager.get_legal_moves(uid, from_square)