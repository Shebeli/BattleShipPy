import pytest

from game.core import Player, BattleShipGame
from game.ship import Ship
from game.exceptions import ShipLengthError, GameConditionError, SquareStrikedError, PlayerDoesNotExist

# player1's user here is considered as str '1', while player2's user is considered '2'.


@pytest.fixture
def empty_core():
    return BattleShipGame('1', '2')


@pytest.fixture
def finished_core():
    c = BattleShipGame('1', '2')
    c.is_finished = True
    return c


@pytest.fixture
def default_core():
    game = BattleShipGame.start_game('1', '2')
    game.started = True
    return game


@pytest.fixture
def core_withoneship(empty_core):
    b1 = empty_core.p1.board
    ship = b1.create_ship([(0, 0), (0, 1)])
    return empty_core


@pytest.fixture
def core_ship(core_withoneship):
    return core_withoneship.p1.board.ships[0]


class TestCore:

    def test_instantiation(self, empty_core):
        assert isinstance(empty_core, BattleShipGame)

    def test_start_game(self):
        core = BattleShipGame.start_game('1', '2')
        assert all(
            [len(p.board.ships) == core.max_ship_count for p in core.players])

    def test_turn_validation(self, default_core):
        with pytest.raises(Exception):
            default_core.turn = 'test'

    def test_get_ship(self, default_core):
        ship = default_core.p1.board.ships[0]
        square = ship.squares[0]
        assert square.ship == default_core.get_ship((square.x, square.y), '1')

    @pytest.mark.parametrize(
        "input,raises_error,error_type",
        [([(6, 5), (6, 6)], False, None),
         ([(6, 5), (6, 6)], True, GameConditionError),
         ([(0, 1), (0, 2), (0, 3)], True, ShipLengthError)]
    )
    def test_move_ship(self, core_withoneship, core_ship, finished_core, input, raises_error, error_type):
        if raises_error:
            with pytest.raises(error_type):
                if error_type == GameConditionError:
                    core_withoneship.finished = True
                    core_withoneship.move_ship(core_ship, input, '1')
                elif error_type == ShipLengthError:
                    core_withoneship.move_ship(core_ship, input, '1')
        else:
            core_withoneship.move_ship(core_ship, input, '1')
            assert core_ship.squares[0].cord == (6, 5)

    @pytest.mark.parametrize(
        "raises_error,error_type",
        [(True, PlayerDoesNotExist),
         (True, SquareStrikedError),
         (False, None)]
    )
    def test_strike(self, default_core, raises_error, error_type):
        p1, p2 = default_core.p1, default_core.p2
        if raises_error:
            with pytest.raises(error_type):
                if error_type == PlayerDoesNotExist:
                    default_core.strike((0, 0), '123')
                elif error_type == SquareStrikedError:
                    sq = p2.board.get_square((0, 0))
                    sq.state = 3
                    default_core.strike((0, 0), '1')
        else:
            default_core.strike((0, 0), '1')
            assert default_core.p2.board.squares[0][0].state in [1, 3]

    # def test_both_map(self, default_core):
    #     print(default_core.player_map('1'))
    #     print(default_core.opponent_map('1'))
    #     assert False
