"""Management class for the AI related functionalities"""

import gymnasium as gym
import shogi

from repository.dataclasses.game import Game
from services.ai.agent import ShogiAgent
from services.ai.environment import ShogiEnv


class AiService:
    """Management class for the AI related functionalities"""

    def __init__(self):
        gym.register(id="Shogi-v0", entry_point="services.ai.environment:ShogiEnv")
        self.env: ShogiEnv = gym.make("Shogi-v0")
        self.env.reset()
        self.agent = ShogiAgent(path="model/shogi-agent.pth")

    def setup_game(self, game: Game):
        """Update the env based on the game settings"""
        for move in game.moves:
            move = self.dict_to_move(
                self.env.board,
                move["from_square"],
                move["to_square"],
                move["promotion"],
            )
            self.env.board.push(move)

    def make_move(self) -> shogi.Move:
        """Have the AI make a move"""
        action, _ = self.agent.select_action(self.env)
        return action

    def dict_to_move(
        self, board: shogi.Board, from_square: str, to_square: str, promote: bool
    ) -> shogi.Move:
        """Transform a move dict, to a shogi.Move object"""
        move = from_square + to_square
        piece_type = board.piece_at(self._square_to_index(from_square)).piece_type
        can_promote = shogi.can_promote(
            self._square_to_index(to_square), piece_type, board.turn
        )
        if promote and can_promote:
            move += "+"

        return shogi.Move.from_usi(move)

    @staticmethod
    def _square_to_index(square):
        """Get the index of the specified square"""
        files = "987654321"  # Shogi files in reverse order
        ranks = "abcdefghi"  # Shogi ranks
        file = files.index(square[0])  # Convert file to index
        rank = ranks.index(square[1])  # Convert rank to index
        return rank * 9 + file
