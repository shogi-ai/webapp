import uuid

from shogi import Move


class Game:
    def __init__(self, moves: list[Move]):
        self.uid = str(uuid.uuid4())
        self.moves = moves

    def to_dict(self):
        moves = [move.__dict__ for move in self.moves]
        return {
            "uid": self.uid,
            "moves": moves,
        }
