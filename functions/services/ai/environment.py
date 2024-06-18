"""Shogi environment for reinforcement learning."""

import random
import shogi

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from shogi import Move

from services.ai.exceptions.illegal_move import IllegalMoveException
from services.ai.exceptions.no_legal_moves import NoMovesException
from services.ai.reward_table import PIECE_REWARDS, STALEMATE, CHECKMATE


class ShogiEnv(gym.Env):
    """
    Shogi environment for reinforcement learning.

    This environment simulates a game of Shogi, a Japanese variant of chess.
    It provides an action space representing all possible moves and an observation space representing the Shogi board.
    The game continues until a player wins, the game reaches a stalemate, or a specified number of moves is reached.
    """

    def __init__(self):
        """
        Initialize the Shogi environment.

        Initializes the Shogi board, action space, and observation space.
        """
        super(ShogiEnv, self).__init__()
        self.board = shogi.Board()

        # Action space represents all possible moves in Shogi
        self.action_space = spaces.MultiDiscrete(
            [81, 81]
        )  # From square (x, y) to square (x, y)
        self.action_space.sample = self.sample_action

        # Observation space represents the Shogi board
        self.observation_space = spaces.MultiDiscrete(
            [81, 17]
        )  # 9x9 board with 17 possible pieces

        # Keep track of moves
        self.move = 0
        self.max_moves = 200

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, any] | None = None,
    ) -> np.array:
        """
        Reset the environment to its initial state.
        """
        self.board = shogi.Board()
        self.move = 0
        return self.get_observation()

    def sample_action(self) -> Move:
        """
        Sample a random legal move for the specified player.
        """
        legal_moves = self.get_legal_moves()
        return random.choice(legal_moves)

    def step(self, action: Move) -> (np.array, float, bool, bool, dict):
        """
        Take a step in the environment based on the action.
        """
        if action not in self.board.legal_moves:
            raise IllegalMoveException()

        self.move += 1
        reward = 0.0
        terminated = False
        truncated = False

        piece = self.board.piece_at(action.to_square)
        if piece:
            piece_name = self._get_piece_name(piece.piece_type)
            reward += PIECE_REWARDS[piece_name]

        self.board.push(action)

        if self.move >= self.max_moves:
            truncated = True

        if self.board.is_checkmate():
            reward += CHECKMATE
            terminated = True
        elif self.board.is_stalemate():
            reward += STALEMATE
            terminated = True

        return self.get_observation(), reward, terminated, truncated, {}

    def get_observation(self) -> np.array:
        """
        Get the current bitboard of the Shogi board.
        """
        piece_symbols = [
            "",
            "p",
            "l",
            "n",
            "s",
            "g",
            "b",
            "r",
            "k",
            "+p",
            "+l",
            "+n",
            "+s",
            "+b",
            "+r",
        ]
        pieces_in_board = [self.board.piece_at(i) for i in range(81)]
        indices = []

        def print_bitboard(piece, pieces_in_board):
            output = []
            for _, x in enumerate(pieces_in_board):
                if str(x).lower() == piece:
                    output.append(1)
                else:
                    output.append(0)
            return np.reshape(output, (9, 9))

        for piece in piece_symbols:
            if piece == "":
                continue
            indices.append(print_bitboard(piece, pieces_in_board))

        return np.array(indices)

    def render(self):
        """
        Render the current state of the Shogi board.
        """
        print("=" * 25)
        print(self.board)

    @staticmethod
    def _get_piece_name(piece_type: int) -> str:
        """
        Get piece name based on piece type.
        """
        piece_types = [
            "PAWN",
            "LANCE",
            "KNIGHT",
            "SILVER",
            "GOLD",
            "BISHOP",
            "ROOK",
            "KING",
            "PROM_PAWN",
            "PROM_LANCE",
            "PROM_KNIGHT",
            "PROM_SILVER",
            "PROM_BISHOP",
            "PROM_ROOK",
        ]
        piece = piece_types[piece_type - 1]
        return piece

    def get_legal_moves(self) -> list[Move]:
        """Get all legal moves"""
        generator = self.board.generate_legal_moves()
        legal_moves = [move for move in generator if move.from_square is not None]
        if len(legal_moves) == 0:
            raise NoMovesException()
        return legal_moves
