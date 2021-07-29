from typing import List, Tuple

from game.square import Square
from game.ship import Ship
from game.exceptions import (CordinatesValidationError, MaxShipReachedError)


class Board:

    def __init__(self, x: int, y: int, max_ship_count: int):
        """For handling squares and ships instances in BattleShipGame class.

        y is an indicator that defines how long each array is,
        while x defines how many arrays should be in board.
        The number of ships on the board cannot exceed max ship count attribute.
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

    def _validate_cordinates(self, *cords):
        for cord in cords:
            i, j = cord[0], cord[1]
            if not 0 <= i <= self.x-1 or not 0 <= j <= self.y-1:
                raise CordinatesValidationError()

    def get_square(self, cord: Tuple[int, int]) -> Square:
        self._validate_cordinates(cord)
        return self._board[cord[0]][cord[1]]

    def get_squares(self, cordinates: List[Tuple[int, int]] = None) -> List[Square]:
        return [self.get_square(cord) for cord in cordinates]

    def update_state(self, state: int, cord: Tuple[int, int]) -> None:
        square = self.get_square(cord)
        square.state = state

    def create_ship(self, cordinates: List[Tuple[int, int]]) -> Ship:
        """Creates a ship at given coordinates.
    
        Given squares should be attached and not occupied.
        """
        if len(self._ships) >= self.max_ship_count:
            raise MaxShipReachedError
        square_objects = self.get_squares(cordinates)
        ship = Ship(square_objects)
        self._ships.append(ship)
        return ship

    def is_finished(self) -> bool:
        for ship in self.ships:
            if not ship.is_destroyed():
                return False
        return True

    def __str__(self):
        string = '\n'
        for line in self._board:
            for square in line:
                string += square.__str__() + ' '
            string += '\n'
        return string
