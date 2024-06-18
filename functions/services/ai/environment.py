"""Shogi environment for reinforcement learning."""

import random
import shogi

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from shogi import Move


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

    def sample_action(self) -> Move:
        """
        Sample a random legal move for the specified player.
        """
        legal_moves = self.get_legal_moves()
        return random.choice(legal_moves)

    def get_observation(self) -> np.array:
        """
        Get the current bitboard of the Shogi board.

        Returns:
            list: List representing the current bitboard of the Shogi board.
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
        pieces_in_hand = self.board.pieces_in_hand
        indices = []

        def print_bitboard(piece, pieces_in_board):
            white_pieces = []
            black_pieces = []
            for _, x in enumerate(pieces_in_board):
                if str(x).lower() == piece:
                    if str(x).isupper():
                        white_pieces.append(1)
                        black_pieces.append(0)
                    else:
                        black_pieces.append(1)
                        white_pieces.append(0)
                else:
                    white_pieces.append(0)
                    black_pieces.append(0)
            return np.reshape(white_pieces, (9, 9)), np.reshape(black_pieces, (9, 9))

        def create_hand_bitboard(pieces_in_hand, index, is_black):
            hand_indices = []
            # Check for white pieces in hand
            if pieces_in_hand[is_black][index] == 0:
                hand_indices.append(np.zeros(81))
            else:
                for _ in range(pieces_in_hand[0][index]):
                    hand_indices.append(1)
                hand_indices.append(np.zeros(81 - len(pieces_in_hand)))

            return np.reshape(hand_indices, (9, 9))

        for piece in piece_symbols:
            if piece == "":
                continue
            white_indices, black_indices = print_bitboard(piece, pieces_in_board)
            indices.append(white_indices)
            indices.append(black_indices)

        # Add hand bitboards
        for i in enumerate(piece_symbols[1:8]):
            white_indices = create_hand_bitboard(pieces_in_hand, i, False)
            black_indices = create_hand_bitboard(pieces_in_hand, i, True)
            indices.append(white_indices)
            indices.append(black_indices)

        return np.array(indices)

    def render(self):
        """
        Render the current state of the Shogi board.
        """
        print("=" * 25)
        print(self.board)

    def get_legal_moves(self) -> list[Move]:
        """Get all legal moves"""
        generator = self.board.generate_legal_moves()
        legal_moves = [move for move in generator]
        return legal_moves
