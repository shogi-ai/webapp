"""Object got the game"""
import uuid


class Game:
    """Object got the game"""

    def __init__(self, moves: list[dict], board: list[list], pieces_in_hand: list[str]):
        self.uid = str(uuid.uuid4())
        self.moves = moves
        self.board = board
        self.pieces_in_hand = pieces_in_hand

    def to_dict(self):
        """Get the game object as a dict"""
        board = [item for sublist in self.board for item in sublist]
        return {
            "uid": self.uid,
            "moves": self.moves,
            "board": board,
            "pieces_in_hand": self.pieces_in_hand,
        }

    @classmethod
    def from_dict(cls, game_dict: dict):
        """Turn a dict into the Game object"""

        board = []
        for i in range(0, 81, 9):
            board.append(game_dict["board"][i : i + 9])
        game = cls(game_dict["moves"], board, game_dict["pieces_in_hand"])
        game.uid = game_dict["uid"]
        return game
