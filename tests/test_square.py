import pytest

from game.square import Square, SquareStatus
from game.exceptions import NotValidChoiceError


@pytest.fixture
def square():
    return Square()


class TestSquares:
    """SquareStatus and Square classes."""

    def test_values(self):
        assert SquareStatus.values() == [0, 1, 2, 3]

    def test_validate(self):
        with pytest.raises(NotValidChoiceError):
            SquareStatus.validate(10)

    def test_state_setter_not_valid(self, square):
        with pytest.raises(NotValidChoiceError):
            square.state = 10

    def test_state_setter_valid(self, square):
        try:
            square.state = 0
        except NotValidChoiceError:
            assert False

    # def test_str(self, square):
    #     print(square)
    #     assert False
