from typing import Type, List, Tuple, Any
from itertools import product, cycle, count
from random import sample, randint, choice

from game.board import Board
from game.ship import Ship
from game.exceptions import (SquareStateError, ShipLengthError, SquareStrikedError,
                             GameConditionError,PlayerDoesNotExist , MaxShipReachedError, PlayerTurnError, StartedOrFinishedError)



class Player:
    def __init__(self, user: Any,  board: Board):
        self.user = user
        self.board = board
        self.ready = False


class BattleShipGame:  # there should be some sort of verification where the player is verified to be the owner of the board, and so they cant access the opponent's board.
    def __init__(self, p1: Any, p2: Any, x=7, y=7, max_ship_count=7):
        self.p1 = Player(p1, Board(x, y, max_ship_count))
        self.p2 = Player(p2, Board(x, y, max_ship_count))
        self.x = x
        self.y = y
        self.max_ship_count = max_ship_count
        self.turn = self.p1
        self._cycle = cycle((self.p2, self.p1))
        self.started = False
        self.finished = False
        self.winner = None

    def _validate_player(self, user: Any):
        users = [p.user for p in self.players]
        if user not in users:
            raise PlayerDoesNotExist("The given player is not in this game")

    def _validate_finish(self):
        if self.winner:
            raise StartedOrFinishedError("Game is finished")

    def get_player(self, user: Any):
        self._validate_player(user)
        return next((p for p in self.players if p.user == user))

    def get_opponent(self, user: Any):
        self._validate_player(user)
        return next((p for p in self.players if p.user != user))

    @property
    def players(self):
        return self.p1, self.p2

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, player):
        if player not in self.players:
            raise PlayerTurnError(
                "player should be one of game's players. use change_turn method instead")
        self._turn = player

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, player: Any):
        if self.finished:
            raise StartedOrFinishedError("The game is already finished")
        if player not in self.players and player is not None:
            raise PlayerDoesNotExist("Should be one of the game's player")
        self._winner = player

    def change_turn(self):
        self.turn = next(self._cycle)

    def setup_ships(self):
        """
        Creates n number of ships based on game's ship count.
        The ships are created randomly at players boards.
        Ships can be only created randomly once.
        """
        self._validate_finish()
        b1 = self.p1.board
        b2 = self.p2.board
        if all([len(x.ships) == self.max_ship_count for x in [b1, b2]]):
            raise MaxShipReachedError
        self._random_ships(b1, b2)

    def _random_ships(self, *boards: Type[Board]):
        lengths = [randint(2, 5) for _ in range(self.max_ship_count)]
        for board in boards:
            board_cords = board.cords
            c = 0
            while len(board.ships) != self.max_ship_count:
                length = lengths[c]
                i, j = choice(board_cords)  # (0,5)
                if 0 <= i + length <= self.x and all([(i+z, j) in board_cords for z in range(length)]):
                    cords = [(i+z, j) for z in range(length)]
                    board.create_ship(cords)
                    for element in cords:
                        board_cords.remove(element)
                    c += 1
                elif 0 <= i - length <= self.x and all([(i-z, j) in board_cords for z in range(length)]):
                    cords = [(i-z, j) for z in range(length)]
                    board.create_ship(cords)
                    for element in cords:
                        board_cords.remove(element)
                    c += 1
                elif 0 <= j + length <= self.y and all([(i, j+z) in board_cords for z in range(length)]):
                    cords = [(i, j+z) for z in range(length)]
                    board.create_ship(cords)
                    for element in cords:
                        board_cords.remove(element)
                    c += 1
                elif 0 <= j - length <= self.y and all([(i, j-z) in board_cords for z in range(length)]):
                    cords = [(i, j-z) for z in range(length)]
                    board.create_ship(cords)
                    for element in cords:
                        board_cords.remove(element)
                    c += 1

    def get_ship(self, cord: Tuple[int, int], user: Any):
        """Returns the ship associated with the given cordinate."""
        player = self.get_player(user)
        square = player.board.get_square(cord)
        return square.ship

    def move_ship(self, ship: Ship, cords: List[Tuple[int, int]], user: Any):
        """
        Moves a ship to the given cordinates.
        """
        if self.started or self.finished:
            raise GameConditionError
        if len(cords) != ship.length:
            raise ShipLengthError
        player = self.get_player(user)
        board = player.board
        new_sqs = board.filter(cords)
        ship.squares = new_sqs

    def strike(self, cord: Tuple[int, int], user: Any):
        """
        Strikes a given cord on board depending on whos turn it is.
        the turn doesn't change if it hits a ship square.
        Missed or hit squares cannot be targeted again.
        """
        player = self.get_player(user)
        if self.finished:
            raise Exception("The game is over")
        if not self.started:
            raise Exception("The game hasnt been started")
        if self._turn != player:
            raise PlayerTurnError("It's not your turn yet.")
        board = self.get_opponent(user).board  # get opponent
        square = board.get_square(cord)
        if square.state in [1, 3]:
            raise SquareStrikedError
        if square.state == 0:
            square.state = 1
            self.change_turn()
        else:
            square.state = 3
            if board.is_finished():
                self.winner = self.turn

    def player_map(self, user: Any):
        """Returns a 2D array showing the player's board"""
        player = self.get_player(user)
        return [[square.state for square in sq_list] for sq_list in player.board.squares]

    def opponent_map(self, user: Any):
        """
        Returns a 2D array showing the player's hidden board.
        This is the map that should be shown to player's opponent.
        """
        player = self.get_player(user)
        opp = self.get_opponent(player)
        return [[self._hide_map(square) for square in sq_list] for sq_list in opp.board.squares]

    @staticmethod
    def _hide_map(square):
        if square.state in [1, 3]:
            return square.state
        return 4

    @classmethod
    def start_game(cls, p1, p2):
        """Used to instantiate core object with given player names and default settings"""
        game = cls(p1, p2)
        game.setup_ships()
        return game

    def __str__(self):
        return f"Players: {self.players}, finished: {self.finished}"

    def __repr__(self):
        return f"finished: {self.finished} started: {self.finished} turn: {self.turn}"
