from typing import Type, List, Tuple

from .exceptions import SquareStateError, SquaresNotAttachedError, ShipLengthError

class Ship:
    def __init__(self, squares: List[Type[Square]]):
        self._squares = squares

    @property
    def squares(self):
        return self._squares

    @state.setter
    def squares(self, value):
        self.validate(squares)
        for square in squares:
            square.state = 2
            square.ship = self
        self._squares = squares

    def validate(self, squares: List[Type[Square]]):
        """
        Validates the length and emptiness of given squares
        and if the squares are attached or not.
        """
        self.validate_empty(squares)
        self.validate_length(squares)
        squares = [(square.x, square.y) for square in squares]
        first_x = squares[0][0]
        first_y = squares[0][1]
        for x, y in squares:  # continues cordinates validation
            if x != first_x and y != first_y:
                raise SquaresNotAttachedError

    @staticmethod
    def validate_length(squares: List[Type[Square]], _min=2, _max=5):
        if not(_min <= len(squares) <= _max):
            raise ShipLengthError

    @staticmethod
    def validate_empty(squares: List[Type[Square]]):
        for square in squares:
            if square.state != 0:
                raise SquareStateError(
                    "The given square is not in empty state")

    @property
    def length(self):
        return len(self.squares)