class Game(object):
    def __init__(self):
        """
        Initialize the game object
        """
        print '[Game] instance initiallized'
        self._pieces = []
        self.set_initial_pieces()

    def add_piece(self, piece):
        """
        Adds a game piece
        """
        self._pieces.append(piece)

    def remove_piece(self, piece):
        """
        Remove a game piece
        """
        self._pieces.remove(piece)

    def get_piece(self, x, y):
        """
        Get a game piece by (x, y)
        """
        for piece in self._pieces:
            if piece.get_coords() == (x, y):
                return piece
        return None

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

    def do_move_effect(self, from_piece, to_piece):
        """
        If a move has an effect (e.g. eating, or any othe special effect),
        implement it in this function
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
        self.do_move_effect(from_piece, to_piece)

        # set the new coordinates for the from piece
        from_piece.set_coords(x_to, y_to)
