from GamePiece import GamePiece
import chess

EMPTY_SQUARE='.'

class ChessPiece(GamePiece):
    color = None

    def __init__(self, piece_type, x, y):
        """
        Initialize the chess piece object
        """
        GamePiece.__init__(self, piece_type, x, y)
