import pytest

from game.square import Square, SquareStatus
from game.exceptions import NotValidChoiceError


@pytest.fixture
def square():
    return Square(0, 0, 3)


class TestSquares:

    def test_values(self):
        assert SquareStatus.values() == [0, 1, 2, 3, 4]

    def test_validation_raises_error(self):
        with pytest.raises(NotValidChoiceError):
            SquareStatus.validate(10)

    def test_setter_raises_error(self, square):
        with pytest.raises(NotValidChoiceError):
            square.state = 10

    def test_setter_no_error(self, square):
        try:
            square.state = 0
        except NotValidChoiceError:
            assert False

    # def test_str(self, square):
    #     print(square)
    #     assert False
