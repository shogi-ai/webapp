"""Class to manage the Shogi board"""

import shogi
from shogi import Piece, Move
from services.board_info import SQUARES, SQUARE_NAMES, COLORS
import numpy as np
import random


class ShogiBoard:
    """Class to manage the Shogi board"""

    def __init__(self):
        self.board = shogi.Board()

    def get_board(self):
        """Get board in format that front end can use"""
        bitboard = []
        pieces_in_hand = []

        for square in SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                bitboard.append(piece.symbol())
            else:
                bitboard.append(None)

        bitboard = [bitboard[i : i + 9] for i in range(0, len(bitboard), 9)]

        for color in COLORS:
            for piece_type, piece_count in self.board.pieces_in_hand[color].items():
                for i in range(piece_count):
                    piece = Piece(piece_type, color)
                    pieces_in_hand.append(piece.symbol())

        return (bitboard, pieces_in_hand)

    @staticmethod
    def _square_to_index(square):
        """Get the index of the specified square"""
        files = "987654321"  # Shogi files in reverse order
        ranks = "abcdefghi"  # Shogi ranks
        file = files.index(square[0])  # Convert file to index
        rank = ranks.index(square[1])  # Convert rank to index
        return rank * 9 + file

    def make_move(self, from_square: str, to_square: str, promote: bool):
        """Make a new move in a game"""
        move = from_square + to_square
        piece_type = self.board.piece_at(self._square_to_index(from_square)).piece_type
        can_promote = shogi.can_promote(
            self._square_to_index(to_square), piece_type, self.board.turn
        )
        if promote and can_promote:
            move += "+"

        self.board.push(shogi.Move.from_usi(move))
        return self.get_board()

    def get_legal_moves(self, from_square):
        """Get all the legal moves"""
        piece_legal_moves = []

        for move in self.board.legal_moves:
            if from_square == move.usi()[:2]:
                piece_legal_moves.append(move.usi()[2:])

        board_builder = []

        for square in SQUARE_NAMES:
            if square in piece_legal_moves:
                board_builder.append(square)
            else:
                board_builder.append(None)

        return [board_builder[i : i + 9] for i in range(0, len(board_builder), 9)]
    
    def get_legal_moves(self) -> list[Move]:
        generator = self.board.generate_legal_moves()
        legal_moves = [move for move in generator]
        if len(legal_moves) == 0:
            return []
        return legal_moves

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
    
    def sample_action(self) -> Move:
        """
        Sample a random legal move for the specified player.

        Returns:
            shogi.Move: Random legal move for the specified player.
        """
        legal_moves = self.get_legal_moves()
        return random.choice(legal_moves)