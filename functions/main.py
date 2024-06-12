"""
Welcome to Cloud Functions for Firebase for Python!
To get started, simply uncomment the below code or create your own.
Deploy with `firebase deploy
"""

from firebase_functions import https_fn, options
from firebase_admin import initialize_app
from services.board import ShogiBoard

app = initialize_app()
shogi_board = ShogiBoard()
    
@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def read_board(req: https_fn.Request) -> https_fn.Response:
    return {
        "board": shogi_board.get_board()
    }

@https_fn.on_request()
def make_move(req: https_fn.Request) -> https_fn.Response:
    move_str = req.args.get("move")
    if move_str is None:
        return https_fn.Response("Invalid move", status=400)
    
    return {
        "board": shogi_board.make_move(move_str)
    }

@https_fn.on_request()
def read_legal_moves(req: https_fn.Request) -> https_fn.Response:
    piece_from_square = req.args.get("from_square")
    if piece_from_square is None:
        return https_fn.Response("Invalid from_square", status=400)
    return {
        "legal_moves": shogi_board.get_legal_moves(piece_from_square)
    }