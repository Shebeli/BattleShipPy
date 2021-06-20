from enum import Enum
from typing import Type, List

from .exceptions import NotValidChoiceError, CordinatesValidationError, SquareStateError
from .square import Square


class Ship:
    def __init__(self, squares: List[Type[Square]]):
        for square in squares:
            if square.state != 0:
                raise SquareStateError(
                    "The given square is not in empty state")
            square.state = 2
        self.squares = squares

    @property
    def length(self):
        return len(self.squares)


class Board:

    def __init__(self, x: int = 10, y: int = 10):
        """
        y is an indicator that defines how long each array is, 
        while x defines how many arrays should be in board.
        """
        self._board = [[Square() for j in range(y)] for i in range(x)]
        self._ships = []

    @property
    def x(self):
        return len(self._board)

    @property
    def y(self):
        return len(self._board[0])

    def _validate_cordinates(self, i: int, j: int) -> None:
        """Validates if the given cordinates are within range of board's x and y."""
        if not(0 <= i <= self.x) or not(0 <= j <= self.y):
            raise CordinatesValidationError

    def access(self, i: int, j: int) -> Type[Square]:
        """Returns square object on x,y cordinates."""
        self._validate_cordinates(i, j)
        return self._board[i][j]

    def update_state(self, state: int, i: int, j: int) -> None:
        """Update the state of a square either by cordinates or the object itself"""
        square = self.access(i, j)
        square.state = state

    def __str__(self):
        string = '\n'
        for line in self._board:
            for square in line:
                string += square.__str__() + ' '
            string += '\n'
        return string
