import uuid

from shogi import Move


class Game:
    def __init__(self, moves: list[Move], board: list[list], pieces_in_hand: list[str]):
        self.uid = str(uuid.uuid4())
        self.moves = moves
        self.board = board
        self.pieces_in_hand = pieces_in_hand

    def to_dict(self):
        moves = [move.__dict__ for move in self.moves]
        board = [item for sublist in self.board for item in sublist]
        return {
            "uid": self.uid,
            "moves": moves,
            "board": board,
            "pieces_in_hand": self.pieces_in_hand,
        }
