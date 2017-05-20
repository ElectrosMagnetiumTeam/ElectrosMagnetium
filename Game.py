class Game(object):
    # Game states
    PLAYING = 0
    WIN = 1
    TIE = 2

    def __init__(self, board_width, board_height):
        """
        Initialize the game object
        """
        print '[Game] instance initiallized'
        self._grid = [[None for y in range(board_height)] for x in range(board_width)] 
        self._state = Game.PLAYING
        self.set_initial_pieces()

    def __str__(self):
        """
        ASCII representation of the game's board
        """
        raise NotImplementedError("Please Implement this method in a subclass")

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

    def is_move_legal(self, from_piece, to_piece):
        """
        checks if the move is legal
        """
        raise NotImplementedError("Please Implement this method in a subclass")

    def execute_move(self, from_piece, to_piece):
        """
        Subclass specific implementation of move that takes care of updating
        the grid and physically moving the pieces according to the game's specific
        pieces animations and grid sizes
        """
        raise NotImplementedError("Please Implement this method in a subclass")

    def get_state(self):
        """
        Returns the game state (PLAYING, WIN, TIE)
        """
        return self._state

    def update_game_state(self, new_state):
        """
        Updates the game state
        """
        self._state = new_state

    def get_victory_string(self):
        """
        Subclass specific implementation.
        If a win condition is reached, the function should return the string name of the winner (i.e. white/black)
        and the reason for the victory.
        """
        raise NotImplementedError("PLease Implement this method in a subclass")

    def get_turn_string(self):
        """
        Subclass specific implementation.
        Get the name of the currently playing team
        """
        raise NotImplementedError("PLease Implement this method in a subclass")

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

        # get the piece that is in the destination (if exists)
        to_piece = self.get_piece(x_to, y_to)

        # check if the move is legal
        if not self.is_move_legal(from_piece, to_piece):
            return False

        # do the move's special effects
        self.execute_move(from_piece, to_piece)

        return True
