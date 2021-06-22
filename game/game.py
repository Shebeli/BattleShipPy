from typing import Type, List, Tuple
from itertools import product
from random import sample, randint, choice

from .board import Board
from .ship import Ship
from .exceptions import ShipLengthError, SquareStrikedError


class Player:
    def __init__(self, name: str,  board: Type[Board]):
        self.name = name
        self.board = board


class Game:
    def __init__(self, p1='player1', p2='player2', x=7, y=7, ship_count=7):
        self.p1 = Player(p1, Board(x, y, ship_count))
        self.p2 = Player(p2, Board(x, y, ship_count))
        self.x = x
        self.y = y
        self.ship_count = ship_count
        self._turn = self.p1
        self.started = False

    @property
    def turn(self):
        return self._turn

    def change_turn(self):
        if self._turn == self.p1:
            self._turn = self.p2
        else:
            self._turn = self.p1

    def setup_ships(self, board: Type[Board]):
        """
        Creates n number of ships based on ship count.
        The ships are created randomly at given board.
        This method should be called for each player's board at the start,
        other wise there will be no ships on that board.
        """
        board_cords = board.cords
        while board.ship_count != self.ship_count:
            length = randint(2, 5)
            i, j = choice(choice(board_cords))  # e.g (0,5)
            # e.g [(0,5), (1,5), (2,5)] for length=3
            cords = [(i+z, j) for z in range(length)]
            if 0 <= i + length <= self.x and cords in board_cords:
                board.create_ship(cords)
                for element in cords:
                    board_cords.remove(element)
            # cords = [(i-z, j) for z in range(length)]
            elif 0 <= i - length <= self.x and cords in board_cords:
                board.create_ship(cords)
                for element in cords:
                    board_cords.remove(element)
            # cords = [(i, j+z) for z in range(length)]
            elif 0 <= j + length <= self.y and cords in board_cords:
                board.create_ship(cords)
                for element in cords:
                    board_cords.remove(element)
            # cords = [(i, j-z) for z in range(length)]
            elif 0 <= j - length <= self.y and cords in board_cords:
                board.create_ship(cords)
                for element in cords:
                    board_cords.remove(element)

    def move_ship(self, ship: Type[Ship], cords: List[Tuple(int, int)], board: Type[Board]):
        """
        Moves a ship to the given cordinates.
        the length cannot be changed.
        the ship object should be updated with the new cordinates.
        this method cannot be called while in game.
        """
        if len(cords) != ship.length:
            raise ShipLengthError
        for square in ship.squares:
            square.ship = None
            square.state = 0
        new_sqs = board.filter(cords)
        ship.squares = new_sqs

    def strike(self, cord: Tuple(int, int)):
        """
        Strikes a given cord on board depending on whos turn it is.
        the turn doesn't change if it hits a ship square.
        Missed squares cannot be targeted again.
        """
        if self._turn == self.p1:
            board = self.p2.board
        else:
            board = self.p1.board
        square = board.get_square(cord[0], cord[1])
        if square.state in [1, 3]:
            raise SquareStrikedError
        if square.state == 0:
            print(f"{self.turn.name} missed!")
            square.state = 1
            self.change_turn()
        else:
            print(f"{self.turn.name} hit a ship!")
            square.state = 3
            # should find a way to see if all the ship are destroyed, and if it is , the game is over
            # add a method to show the map for the opponent
            # add an attribute for finished game??????