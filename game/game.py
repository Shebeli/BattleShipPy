from typing import Type, List, Tuple
from itertools import product
from random import sample, randint, choice

from .board import Board
from .ship import Ship
from .exceptions import ShipLengthError, SquareStrikedError, GameStartedError, MaxShipReachedError


class Player:
    def __init__(self, name: str,  board: Type[Board]):
        self.name = name
        self.board = board


class Game:  # there should be some sort of verification where the player is verified to be the owner of the board, and so they cant access the opponent's board.
    def __init__(self, p1='player1', p2='player2', x=7, y=7, ship_count=7):
        self.p1 = Player(p1, Board(x, y, ship_count))
        self.p2 = Player(p2, Board(x, y, ship_count))
        self.x = x
        self.y = y
        self.ship_count = ship_count
        self._turn = self.p1
        self.started = False
        self._winner = None

    @property
    def turn(self):
        return self._turn

    @property
    def winner(self):
        return self._winner

    @property
    def players(self):
        return self.p1, self.p2

    @setter.winner
    def winner(self, player):
        if player not in [self.p1, self.p2]:
            raise Exception("Should be one of the game's player")
        self._winner = player

    def change_turn(self):
        if self._turn == self.p1:
            self._turn = self.p2
        else:
            self._turn = self.p1

    def setup_ships(self):
        """
        Creates n number of ships based on game's ship count.
        The ships are created randomly at given board.
        """
        b1 = self.p1.board
        # len(b1.ships) == self.ship_count and len(b2.ships) == self.ship_count:
        b2 = self.p2.board
        if all([len(x.ships) == self.ship_count for x in [b1, b2]]):
            raise MaxShipReachedError
        self._random_ships(b1, b2)

    def _random_ships(self, *boards: Type[Board]):
        for board in boards:
            board_cords = board.cords
            while board.ship_count != self.ship_count:
                length = randint(2, 5)
                i, j = choice(choice(board_cords))  # (0,5)
                cords = [(i+z, j) for z in range(length)]
                if 0 <= i + length <= self.x and cords in board_cords:
                    board.create_ship(cords)
                    for element in cords:
                        board_cords.remove(element)
                cords = [(i-z, j) for z in range(length)]
                elif 0 <= i - length <= self.x and cords in board_cords:
                    board.create_ship(cords)
                    for element in cords:
                        board_cords.remove(element)
                cords = [(i, j+z) for z in range(length)]
                elif 0 <= j + length <= self.y and cords in board_cords:
                    board.create_ship(cords)
                    for element in cords:
                        board_cords.remove(element)
                cords = [(i, j-z) for z in range(length)]
                elif 0 <= j - length <= self.y and cords in board_cords:
                    board.create_ship(cords)
                    for element in cords:
                        board_cords.remove(element)

    def get_ship(self, cord: Tuple(int, int), player: Type[Player]):
        """Returns the ship associated with the square"""
        square = self.get_square(cord[0], cord[1])
        return square.ship

    def move_ship(self, ship: Type[Ship], cords: List[Tuple(int, int)], player: Type[Player]):
        """
        Moves a ship to the given cordinates.
        the length cannot be changed.
        the ship object should be updated with the new cordinates.
        this method cannot be called while in game.
        """
        board = player.board
        if self.started:
            raise GameStartedError
        if len(cords) != ship.length:
            raise ShipLengthError
        for square in ship.squares:
            square.ship = None
            square.state = 0
        new_sqs = board.filter(cords)
        ship.squares = new_sqs

    def strike(self, cord: Tuple(int, int), player: Type[Player]):
        """
        Strikes a given cord on board depending on whos turn it is.
        the turn doesn't change if it hits a ship square.
        Missed squares cannot be targeted again.
        """
        if self._turn != player:
            raise Exception(f"It's not {player.name}'s turn yet.")
        players = list(self.players).remove(player)
        board = players[0].board  # opponent
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
            if board.is_finished():
                print(f"{self.turn.name} won!")
                self.winner = self.turn

    def player_map(self, player: Type[Player]):
        """Returns a 2D array showing the player's board"""
        return [[square.state for square in sq_list] for sq_list in player.board.squares]

    @staticmethod
    def _hide_map(square):
        if square.state in [1, 3]:
            return square.state
        return 4

    def hidden_map(self, player: Type[Player]):
        """Returns a 2D array showing the player's hidden board"""
        return [[self._hide_map(square) for square in sq_list] for sq_list in player.board.squares]

    @classmethod
    def start_game(cls, p1='player1', p2='player2'):
        game = cls(p1, p2)
        game.setup_ships()
        return game
