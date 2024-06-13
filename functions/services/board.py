import shogi
from shogi import Piece
from services.board_info import SQUARES, SQUARE_NAMES, COLORS

class ShogiBoard:
    def __init__(self):
        self.board = shogi.Board()

    def get_board(self):
        bitboard = []
        pieces_in_hand = []

        for square in SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                bitboard.append(piece.symbol())
            else:
                bitboard.append(None)

        bitboard = [bitboard[i:i + 9] for i in range(0, len(bitboard), 9)]

        for color in COLORS:
            for piece_type, piece_count in self.board.pieces_in_hand[color].items():
                for i in range(piece_count):
                    piece = Piece(piece_type, color)
                    pieces_in_hand.append(piece.symbol())

        return (bitboard, pieces_in_hand)

    def make_move(self, move):
        self.board.push(shogi.Move.from_usi(move))
        return self.get_board()
    
    def get_legal_moves(self, from_square):
        piece_legal_moves = []

        for move in self.board.legal_moves:
            if from_square == move.usi()[:2]:
                piece_legal_moves.append( move.usi()[2:])

        board_builder = []

        for square in SQUARE_NAMES:
            if square in piece_legal_moves:
                board_builder.append(square)
            else:
                board_builder.append(None)

        return [board_builder[i:i + 9] for i in range(0, len(board_builder), 9)]