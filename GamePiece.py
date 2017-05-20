class GamePiece(object):
    def __init__(self, piece_type, x, y):
        """
        Initialize the game piece object
        """
        print '[GamePiece] Instance initiallized of type "{}" at ({}, {})'.format(piece_type, x, y)
        self._type = piece_type
        self._x = x
        self._y = y

    def get_coords(self):
        """
        Returns the coordinates of the piece
        """
        return (self._x, self._y)

    def set_coords(self, x, y):
        """
        Sets the game piece coordinates
        """
        self._x = x
        self._y = y

    def get_type(self):
        """
        Returns the type of the piece
        """
        return self._type

    def set_type(self, piece_type):
        """
        Sets the type of the piece 
        """
        self._type = piece_type
