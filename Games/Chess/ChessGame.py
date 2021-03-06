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
    GRAVEYARD_WIDTH = 0
    PLAYING_FIELD_WIDTH = 8
    BOARD_HEIGHT = 8
    BOARD_WIDTH = 8 # GRAVEYARD_WIDTH + PLAYING_FIELD_WIDTH

    def __init__(self, hardware, 
                 fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                 graveyard_fen='8/8/8/8'):
        """
        Initialize the chess game object.
        """
        self._chess_board = chess.Board(fen)
        self._fen = fen
        self._graveyard = self._fen_to_array(graveyard_fen)
        self._hardware = hardware
        Game.__init__(self, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        print '[ChessGame] instance initiallized with FEN: "{}" and graveyard FEN: "{}"'.format(fen, graveyard_fen)

    def __str__(self):
        '''
        ASCII representation of the chess board
        '''
        grid_str = ""

        grid_str += ' ' + '-'*(self.BOARD_WIDTH + self.GRAVEYARD_WIDTH) + '\n'

        for y in range(self.BOARD_HEIGHT):
            grid_str += str(self.PLAYING_FIELD_WIDTH - y) + '|'
            for x in range(self.BOARD_WIDTH):
                grid_str += self._grid[x][y].get_type()
            grid_str += "|\n"

        grid_str += ' ' + '-'*(self.BOARD_WIDTH + self.GRAVEYARD_WIDTH) + '\n'
        grid_str += ' ' * 4 + 'abcdefgh'

        return grid_str

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
        x = chr(ord('A') + x - self.GRAVEYARD_WIDTH).lower()
        y = str(y + 1)
        return (x,y)

    def _board_to_grid(self, x, y):
        '''
        Convert a chess piece's board normal x,y coordinates to the grid's coordinates 
        '''
        # Add the graveyard offset 
        x += self.GRAVEYARD_WIDTH 
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

    def get_victory_string(self):
        """
        Returns wether the winner is black or white and the reason for the victory
        The possible reasons are: checkmate, stalemate, insufficient material, 
        seventyfive-move rule, fivefold repetition or a variant end condition.
        """
        team = "white" if self._chess_board.result() == '1-0' else "black"

        if self._chess_board.is_checkmate():
            reason = "checkmate"
        elif self._chess_board.is_stalemate():
            reason = "stalemate"
        elif self._chess_board.is_insufficient_material():
            reason = "insufficient material"
        elif self._chess_board.is_seventyfive_moves():
            reason = "seventy five moves"
        elif self._chess_board.is_fivefold_repetition():
            reason = "fivefold repetition"
        else:
            reason = "unknown"

        return (team, reason)

    def get_turn_string(self):
        """
        Get the name of the currently playing team
        """
        return "white" if self._chess_board.turn else "black" 

    def is_move_legal(self, from_piece, to_piece):
        """
        checks if the move is legal
        """
        if self._chess_board.is_legal(self.get_move(from_piece, to_piece)):
            return True
        else:
            return False

    def get_move(self, from_piece, to_piece):
        '''
        Returns a chess move object from the given pieces
        '''
        x = self._grid_to_board(*from_piece.get_coords())
        y = self._grid_to_board(*to_piece.get_coords())

        return chess.Move.from_uci(''.join((x + y))) 

    def move(self, x_from, y_from, x_to, y_to):
        """
        Calls the superclass move() and updates the game state
        """
        was_move_legal = super(ChessGame, self).move(x_from, y_from, x_to, y_to)

        if self._chess_board.is_game_over():
            if self._chess_board.is_checkmate():
                self.update_game_state(Game.WIN)
            else:
                self.update_game_state(Game.TIE)
        
        return was_move_legal
    
    def execute_move(self, from_piece, to_piece):
        """
        Subclass specific implementation of move that takes care of updating
        the grid and physically moving the pieces according to the game's specific
        pieces animations and grid sizes
        """
        # Update the internal chess board
        move = self.get_move(from_piece, to_piece)
        self._chess_board.push(move)

        self._hardware.move([from_piece.get_coords(), to_piece.get_coords()])

        # Make the from_piece empty and the to_piece have the from_piece's type
        to_piece.set_type(from_piece.get_type())
        from_piece.set_type(EMPTY_SQUARE)
