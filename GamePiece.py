class GamePiece(object):
    def __init__(self, _type, x, y):
        """
        Initialize the game piece object
        """
        print '[GamePiece] instance initiallized in ({}, {})'.format(_type, x, y)
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
