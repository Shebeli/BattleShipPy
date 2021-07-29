from typing import List

from game.exceptions import (SquareStateError, SquaresNotAttachedError,
                             ShipLengthError)
from game.square import Square


class Ship:
    def __init__(self, squares: List[Square]):
        self.squares = squares

    @property
    def squares(self):
        return self._squares

    @property
    def cords(self):
        return [sq.cord for sq in self.squares]

    @squares.setter
    def squares(self, new_squares: List[Square]):
        self._validate(new_squares)
        try:
            for square in self.squares:
                square.state = 0
                square.ship = None
        except AttributeError:
            pass
        for square in new_squares:
            square.state = 2
            square.ship = self
        self._squares = new_squares

    def _validate(self, squares: List[Square]) -> None:
        """Validates the length, emptiness and attachness of given squares."""
        self._validate_empty(squares)
        self._validate_length(squares)
        squares = [(square.x, square.y) for square in squares]
        first_x = squares[0][0]
        first_y = squares[0][1]
        for x, y in squares:  # validates that coordinates are continues
            if x != first_x and y != first_y:
                raise SquaresNotAttachedError

    @staticmethod
    def _validate_length(squares: List[Square], min_=2, max_=5) -> None:
        if not min_ <= len(squares) <= max_:
            raise ShipLengthError

    @staticmethod
    def _validate_empty(squares: List[Square]) -> None:
        for square in squares:
            if square.state != 0:
                raise SquareStateError(
                    "The given square is not in empty state")

    @property
    def length(self):
        return len(self.squares)

    def is_destroyed(self):
        for square in self.squares:
            if square.state != 3:
                return False
        return True

    def __repr__(self):
        return f"LENGTH: {self.length}, SQUARES: {self.squares}"
