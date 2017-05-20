class Game(object):
    def __init__(self, board_width, board_height):
        """
        Initialize the game object
        """
        print '[Game] instance initiallized'
        self._grid = [[None for y in range(board_height)] for x in range(board_width)] 
        self.set_initial_pieces()

    def place_piece(self, piece, x, y):
        """
        Place a game piece in the grid if it's empty 
        """
        if None == self._grid[x, y]:
            self._grid[x][y] = value
            return True
        else:
            return False

    def remove_piece(self, x, y):
        """
        Remove a game piece
        """
        self._grid[x][y] = None

    def get_piece(self, x, y):
        """
        Get a game piece by (x, y)
        """
        return self._grid[x][y]

    def set_initial_pieces(self):
        """
        Sets the initial game pieces
        """
        raise NotImplementedError("Please Implement this method in a subclass")

    def is_move_legal(self, x_from, y_from, x_to, y_to):
        """
        checks if the move from (x_from, y_from) to (x_to, y_to) is legal
        """
        raise NotImplementedError("Please Implement this method in a subclass")

    def execute_move(self, from_piece, to_piece):
        """
        Subclass specific implementation of move that takes care of updating
        the grid and physically moving the pieces according to the game's specific
        pieces animations and grid sizes
        """
        raise NotImplementedError("Please Implement this method in a subclass")

    def move(self, x_from, y_from, x_to, y_to):
        """
        Does a game move.
        Returns if the move was actually done
        """
        # get the from piece
        from_piece = self.get_piece(x_from, y_from)

        # check for it's existence
        if from_piece is None:
            return False

        # check if the move is legal
        if not self.is_move_legal(x_from, y_from, x_to, y_to):
            return False

        # get the piece that is in the destination (if exists)
        to_piece = self.get_piece(x_to, y_to)

        # do the move's special effects
        self.execute_move(from_piece, to_piece)
