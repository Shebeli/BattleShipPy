import pytest

from game.board import Board, Ship
from game.square import Square
from game.exceptions import (CordinatesValidationError, NotValidChoiceError, MaxShipReachedError,
                             ShipLengthError, SquareStateError, SquaresNotAttachedError)

# fuck glyph


@pytest.fixture
def squares():
    return [Square(0, i) for i in range(5)]


@pytest.fixture
def random_squares():
    return [Square(i, i) for i in range(5)]


@pytest.fixture
def many_squares():
    return [Square(0, i) for i in range(15)]


@pytest.fixture
def ship_squares():
    squares = [Square(0, i) for i in range(5)]
    for sq in squares:
        sq.state = 2
    return squares


@pytest.fixture
def destroyed_squares():
    squares = [Square(0, i) for i in range(5)]
    for sq in squares:
        sq.state = 3
    return squares


@pytest.fixture
def ship(squares):
    return Ship(squares)


class TestShip:
    """Test Ship class"""

    def test_instantiation(self, ship):
        assert isinstance(ship, Ship) and ship.length == 5

    def test_ship_updates_square(self, ship):
        old_sqs = ship.squares
        for sq in ship.squares:
            if sq.state != 2:
                assert False
        new_sqs = [Square(0, i) for i in range(5)]
        ship.squares = new_sqs
        for sq in ship.squares:
            if sq.state != 2:
                assert False
        for sq in old_sqs:
            if sq.state != 0:
                assert False

    @pytest.mark.parametrize(
        "raise_error,error_type",
        [(True, ShipLengthError),
         (True, SquareStateError),
         (True, SquaresNotAttachedError),
         (False, None)],
    )
    def test_ship_validators(self, many_squares, ship_squares, random_squares, squares, raise_error, error_type, destroyed_squares):
        if raise_error:
            with pytest.raises(error_type):
                if error_type == ShipLengthError:
                    ship = Ship(many_squares)
                elif error_type == SquareStateError:
                    ship = Ship(ship_squares)
                else:
                    ship = Ship(random_squares)
        else:
            ship = Ship(squares)

    def test_ship_is_not_destroyed(self, squares):
        ship = Ship(squares)
        assert not(ship.is_destroyed())

    def test_ship_is_destroyed(self, squares):
        ship = Ship(squares)
        for sq in squares:
            sq.state = 3
        assert ship.is_destroyed()


@pytest.fixture
def board():
    return Board(7, 7, 7)


@pytest.fixture
def board_wship(board):
    board.create_ship([(0, 1), (0, 2), (0, 3)])
    return board


class TestBoard:
    """Test Board and related classes and stuff."""

    def test_length(self, board):
        assert board.x == 7 and board.y == 7

    @pytest.mark.parametrize(
        "input,raise_error,error_type",
        [((0, 5), False, None), ((11, 22), True, CordinatesValidationError)]
    )
    def test_board_validators(self, board, input, raise_error, error_type):
        if raise_error is False:
            board._validate_cordinates(input)
        else:
            with pytest.raises(error_type):
                board._validate_cordinates(input)

    def test_get_square(self, board):
        # maybe some other ways? there's no other way
        assert isinstance(board.get_square(0, 0), Square)

    @pytest.mark.parametrize(
        "i,j,state,raise_error,error_type",
        [(0, 0, 2, False, None),
         (0, 0, 12, True, NotValidChoiceError),
         (0, 15, 2, True, CordinatesValidationError)]
    )
    def test_update_state(self, board, i, j, state, raise_error, error_type):
        if raise_error:
            with pytest.raises(error_type):
                sq = board.get_square(i, j)
                board.update_state(state, i, j)
        else:
            sq = board.get_square(i, j)
            board.update_state(state, i, j)

    @pytest.mark.parametrize(
        "cords,raise_error,error_type, dummy",
        [([(0, 1), (0, 2)], True, MaxShipReachedError, True),
         #   ([(0, 1), (0, 2)], True, SquareStateError, False),
         ([(0, 1), (0, 2)], False, None, False)
         ]
    )
    def test_create_ship(self, board, cords, raise_error, error_type, dummy):
        if raise_error:
            if dummy:
                for i in range(7):
                    board._ships.append(i)
            with pytest.raises(error_type):
                board.create_ship(cords)
        else:
            board.create_ship(cords)
            assert len(board.ships) == 1

    def test_board_is_over(self, board_wship):
        cords = [(0, 1), (0, 2), (0, 3)]
        for cord in cords:
            i, j = cord[0], cord[1]
            board_wship.update_state(3, i, j)
        assert board_wship.is_finished()

    def test_board_is_not_over(self, board_wship):
        assert not(board_wship.is_finished())

    # def test_str(self, board):
    #     print(board)
    #     assert False
