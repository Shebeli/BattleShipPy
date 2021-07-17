from typing import Type, List, Tuple
from itertools import product, cycle, count
from random import sample, randint, choice

from game.board import Board
from game.ship import Ship
from game.exceptions import SquareStateError, ShipLengthError, SquareStrikedError, GameConditionError, MaxShipReachedError
from api.models.user import User

class Player:
    def __init__(self, user: User,  board: Board):
        self.user = User
        self.board = board
        self.ready = False

class BattleShipGame:  # there should be some sort of verification where the player is verified to be the owner of the board, and so they cant access the opponent's board.
    def __init__(self, p1: User, p2: User, x=7, y=7, max_ship_count=7):
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

    def _player(self, num):
        if num == 1:
            return self.p1
        elif num == 2:
            return self.p2
        raise Exception("Given argument should be either integer 1 or 2")

    def _validate_finish(self):
        if self.winner:
            raise Exception("Game is finished")

    @property
    def players(self):
        return self.p1, self.p2

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, player):
        if player not in self.players:
            raise Exception(
                "player should be one of game's players. use change_turn method instead")
        self._turn = player

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, player):
        if self.finished:
            raise Exception("The game is already finished")
        if player not in self.players and player is not None:
            raise Exception("Should be one of the game's player")
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
        # len(b1.ships) == self.ship_count and len(b2.ships) == self.ship_count:
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

    def get_ship(self, cord: Tuple[int, int], p_num: int):
        """Returns the ship associated with the given cordinate."""
        player = self._player(p_num)
        square = player.board.get_square(cord[0], cord[1])
        return square.ship

    def move_ship(self, ship: Ship, cords: List[Tuple[int, int]], p_num: int):
        """
        Moves a ship to the given cordinates.
        """
        if self.started or self.finished:
            raise GameConditionError
        if len(cords) != ship.length:
            raise ShipLengthError
        player = self._player(p_num)
        board = player.board
        new_sqs = board.filter(cords)
        # if any([sq.state != 0 for sq in new_sqs]):
        #     raise SquareStateError("One of the squares are not empty")
        ship.squares = new_sqs

    def strike(self, cord: Tuple[int, int], p_num: int):
        """
        Strikes a given cord on board depending on whos turn it is.
        the turn doesn't change if it hits a ship square.
        Missed squares cannot be targeted again.
        eg. player 1 strikes 0,0 cordinate and player2's board will be targeted 
        """
        player = self._player(p_num)
        if self._turn != player:
            raise Exception(f"It's not {player.name}'s turn yet.")
        opp = next((p for p in self.players if p != player))  # get opponent
        # players = list(self.players).remove(player)
        board = opp.board
        square = board.get_square(cord[0], cord[1])
        if square.state in [1, 3]:
            raise SquareStrikedError
        if square.state == 0:
            square.state = 1
            self.change_turn()
        else:
            square.state = 3
            if board.is_finished():
                self.winner = self.turn

    def player_map(self, p_num: int):
        """Returns a 2D array showing the player's board"""
        player = self._player(p_num)
        return [[square.state for square in sq_list] for sq_list in player.board.squares]

    def opponent_map(self, p_num: int):
        """
        Returns a 2D array showing the player's hidden board.
        This is the map that should be shown to player's opponent.
        """
        player = self._player(p_num) # input should be main user, but returns the opponent user's map.
        return [[self._hide_map(square) for square in sq_list] for sq_list in player.board.squares]

    @staticmethod
    def _hide_map(square):
        if square.state in [1, 3]:
            return square.state
        return 4

    @classmethod
    def start_game(cls, p1, p2):
        """Used to istantiate a core object with given player names and default settings"""
        game = cls(p1, p2)
        game.setup_ships()
        return game
