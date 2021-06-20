import pytest

from game.board import Board, Ship
from game.square import Square
from game.exceptions import CordinatesValidationError, NotValidChoiceError


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def squares():
    squares = []
    for i in range(5):
        squares.append(Square())
    return squares


@pytest.fixture
def ship(squares):
    return Ship(squares)


class TestShip:
    """Test Ship class"""

    def test_instantiation(self, ship):
        assert isinstance(ship, Ship) and ship.length == 5


class TestBoard:
    """Test Board and related classes and stuff."""

    def test_length(self, board):
        assert board.x == 10 and board.y == 10

    def test_cordinates_validation_not_valid(self, board):
        with pytest.raises(CordinatesValidationError):
            board._validate_cordinates(11, 22)

    def test_cordinates_validation_valid(self, board):
        try:
            board._validate_cordinates(0, 10)
        except CordinatesValidationError:
            assert False

    def test_access(self, board):
        assert isinstance(board.access(0, 0), Square)  # maybe some other ways?

    def test_update_state(self, board):
        square = board.access(0, 0)
        board.update_state(2, 0, 0)
        assert square.state == 2

    def test_update_invalid_state(self, board):
        square = board.access(0, 0)
        with pytest.raises(NotValidChoiceError):
            board.update_state(12, 0, 0)

    # def test_str(self, board):
    #     print(board)
    #     assert False
