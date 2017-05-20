from Game import Game
from ChessPiece import ChessPiece, EMPTY_SQUARE
import ArduinoSerial
import chess # python-chess
import re

'''
A regular FEN representation would show the following:
                           castling ability
                                          | en passant target square
                                          | |
                                          | |    fullmove counter
                                          v v    v
8/5N2/4p2p/5p1k/1p4rP/1P2Q1P1/P4P1K/5q2 w - - 15 44
|                                     | ^      ^
 -------------------------------------  |      L halfmove clock
               |__ piece placement      |
                                      Side to move (white)

We also use the FEN piece placement format to describe the status of the physical
'graveyard' on our board's implementation. The graveyard's representation on the class'
creation is important for 'save file' restoration.
'''
class ChessGame(Game):
    GRAVEYARD_WIDTH = 2
    PLAYING_FIELD_WIDTH = 8
    BOARD_HEIGHT = 8
    BOARD_WIDTH = 12 # GRAVEYARD_WIDTH + PLAYING_FIELD_WIDTH

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                       graveyard_fen='8/8/8/8', hardware):
        """
        Initialize the chess game object.
        """
        self._chess_board = chess.Board(fen)
        self._fen = fen
        self._graveyard = self._fen_to_array(graveyard_fen)
        self._hardware = hardware
        Game.__init__(self, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        print '[ChessGame] instance initiallized with FEN: "{}" and graveyard FEN: "{}"'.format(fen, graveyard_fen)

    def _fen_to_array(self, fen):
        '''
        Convert a fen string to an array
        '''
        pieces = []
        # Each row is represented as a 'rank' in FEN and divided by a /
        for rank in fen.split("/"):
            symbols_filter = re.compile("[kqbnrpKQBNRP]|\d")
            symbols = symbols_filter.findall(rank)
            # Add digits as n digits * '.' to represent an empty square
            for symbol in symbols:
                if symbol.isdigit():
                    pieces += [EMPTY_SQUARE] * int(symbol) 
                else:
                    pieces.append(symbol)

        return pieces

    def _grid_to_board(self, x, y):
        '''
        Convert a chess piece's grid x,y coordinates to a normal chess board's coordinates
        '''
        # Chess columns are represented with letters while rows are numbers
        x = chr(ord('a') + x + self.GRAVEYARD_WIDTH)
        y = str(y) 
        return (x,y)

    def _board_to_grid(self, x, y):
        '''
        Convert a chess piece's board normal x,y coordinates to the grid's coordinates 
        '''
        # Chess columns are represented with letters while rows are numbers
        x = ord(x) - ord('a')
        y = int(y) 
        return (x,y)

    # Get, place and remove piece were overwritten since we are working with a different
    # grid than the user input because of the graveyard mechanics
    def get_piece(self, x, y):
        """
        Get a game piece by (x, y). 
        """
        x, y = self._board_to_grid(x, y)
        return self._grid[x][y]

    def place_piece(self, piece, x, y):
        """
        Place a game piece in the grid if it's empty 
        """
        x, y = self._board_to_grid(x, y)
        if None == self._grid[x, y]:
            self._grid[x][y] = value
            return True
        else:
            return False

    def remove_piece(self, x, y):
        """
        Remove a game piece
        """
        x, y = self._board_to_grid(x, y)
        self._grid[x][y] = None

    def set_initial_pieces(self):
        """
        Sets the initial game pieces
        """
        # Start from the bottom left corner
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                # The content of the first and last 2 columns needs to be parsed from
                # the graveyard FEN while the regular chess board's content is taken
                # from the internal chess board object. 
                if self.GRAVEYARD_WIDTH > x:
                    self._grid[x][y] = ChessPiece(self._graveyard[x+y], x, y)
                elif (self.PLAYING_FIELD_WIDTH + self.GRAVEYARD_WIDTH) <= x:
                    self._grid[x][y] = ChessPiece(self._graveyard[(x - self.PLAYING_FIELD_WIDTH) + y], x, y)
                else:
                    piece = self._chess_board.piece_at((x - self.GRAVEYARD_WIDTH) + (y * self.PLAYING_FIELD_WIDTH))
                    if piece:
                        self._grid[x][y] = ChessPiece(str(self._chess_board.piece_at((x - self.GRAVEYARD_WIDTH) + 
                                                                          (y * self.PLAYING_FIELD_WIDTH))), 
                                                                          x, y)
                    else:
                        # Empty squares are initialized with ChessPieces of type '.' for now for easier debugging.
                        # TODO: Replace with None later?
                        self._grid[x][y] = ChessPiece(EMPTY_SQUARE, x, y)

    def is_move_legal(self, x_from, y_from, x_to, y_to):
        """
        checks if the move from (x_from, y_from) to (x_to, y_to) is legal
        """
        pass

    def execute_move(self, from_piece, to_piece):
        """
        Subclass specific implementation of move that takes care of updating
        the grid and physically moving the pieces according to the game's specific
        pieces animations and grid sizes
        """
        _hardware.move(list(self._board_to_grid(*from_piece.get_coords())))
