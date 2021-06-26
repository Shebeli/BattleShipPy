from typing import Type, List, Tuple

from game.square import Square
from game.ship import Ship
from game.exceptions import (NotValidChoiceError, CordinatesValidationError, SquareStateError, ShipLengthError,
                         SquaresNotAttachedError, MaxShipReachedError)


class Board:

    def __init__(self, x: int, y: int, max_ship_count: int):
        """
        y is an indicator that defines how long each array is,
        while x defines how many arrays should be in board.
        ships are created with random length through random places.
        """
        self._board = [[Square(i, j) for j in range(y)] for i in range(x)]
        self._ships = []
        self.max_ship_count = max_ship_count

    @property
    def squares(self):
        return self._board

    @property
    def x(self):
        return len(self._board)

    @property
    def y(self):
        return len(self._board[0])

    @property
    def ships(self):
        return self._ships
        

    @property
    def cords(self):
        return [square.cord for sq_list in self._board for square in sq_list]

    def _validate_cordinates(self, *cordinates):
        for cord in cordinates:
            i, j = cord[0], cord[1]
            if not(0 <= i <= self.x) or not(0 <= j <= self.y):
                raise CordinatesValidationError()

    def get_square(self, i: int, j: int) -> Type[Square]:
        self._validate_cordinates((i, j))
        return self._board[i][j]

    def filter(self, cordinates: List[Tuple[int, int]] = None) -> List[Type[Square]]:
        return [self.get_square(x, y) for x, y in cordinates]

    def update_state(self, state: int, i: int, j: int) -> None:
        square = self.get_square(i, j)
        square.state = state

    def create_ship(self, cordinates: List[Tuple[int, int]]):
        """
        Creates a ship at given cordinates;
        Given squares should be attached and not occupied.
        """
        if len(self._ships) >= self.max_ship_count:
            raise MaxShipReachedError
        square_objects = self.filter(cordinates)
        ship = Ship(square_objects)
        self._ships.append(ship)

    def is_finished(self):
        for ship in self.ships:
            print(ship, ship.is_destroyed())
            if not(ship.is_destroyed()):
                return False
        return True

    def __str__(self):
        string = '\n'
        for line in self._board:
            for square in line:
                string += square.__str__() + ' '
            string += '\n'
        return string
