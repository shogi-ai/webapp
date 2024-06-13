"""
Welcome to Cloud Functions for Firebase for Python!
To get started, simply uncomment the below code or create your own.
Deploy with `firebase deploy
"""

from firebase_functions.https_fn import (
    on_call,
    CallableRequest,
    HttpsError,
    FunctionsErrorCode,
)
from firebase_functions import options
from firebase_admin import initialize_app
from services.game import GameService

app = initialize_app()
options.set_global_options(region=options.SupportedRegion.EUROPE_WEST1)


@on_call(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def create_game(_: CallableRequest):
    """Endpoint to create a game"""
    game_manager = GameService(app)
    return game_manager.create()


@on_call(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def make_move(req: CallableRequest):
    """Endpoint to make a new move"""
    from_square = req.data.get("from_square")
    to_square = req.data.get("to_square")
    uid = req.data.get("uid")
    promotion = req.data.get("promotion")

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
    if promotion is None:
        promotion = True

    game_manager = GameService(app)
    return game_manager.make_move(uid, from_square, to_square, promotion)


@on_call(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def read_legal_moves(req: CallableRequest):
    """Endpoint to get the legal moves"""
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

    game_manager = GameService(app)
    return game_manager.get_legal_moves(uid, from_square)
