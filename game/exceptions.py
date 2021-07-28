from typing import Any, Tuple


class SquareStateError(Exception):
    pass


class BaseError(Exception):
    def __init__(self, span: Any, message: str):
        self.message = message
        self.span = span

    def __str__(self):
        return f'{self.message}: {self.span}'


class NotValidChoiceError(BaseError):
    """Exception raised if the provided value is not in range of given choices"""

    def __init__(self, span: list = [0, 1, 2, 3], message: str = 'The given value is not in range of given choices'):
        super().__init__(span, message)


class CordinatesValidationError(BaseError):
    """Exception raised if the provided value is not in range of given cordinates"""

    def __init__(self, span: Tuple[int, int] = (10, 10), message: str = "The given values are not valid cordinates"):
        super().__init__(span, message)


class ShipLengthError(BaseError):
    """Exception raised if given length is not appropriate"""

    def __init__(self, span: range = (2, 5), message: str = 'The given length is not appropriate'):
        super().__init__(span, message)


class SquaresNotAttachedError(Exception):
    """Exception raised if given squares are not attached"""

    def __init__(self, message: str = 'The given squares are not attached'):
        super().__init__(message)


class MaxShipReachedError(Exception):
    """Exception raised if the board reached its maximum ship count"""

    def __init__(self, message: str = 'maximum ship count on board is reached'):
        super().__init__(message)


class SquareStrikedError(Exception):
    """Exception raised if the square is already striked"""

    def __init__(self, message: str = 'Selected square has already been striked, choose another'):
        super().__init__(message)


class GameConditionError(Exception):
    """Exception raised if the provoked action cannot be done when the game has started or finished"""

    def __init__(self, message: str = 'Cannot do the selected action since the game has already been started or finished'):
        super().__init__(message)


class PlayerTurnError(Exception):
    pass


class StartedOrFinishedError(Exception):
    pass


class PlayerDoesNotExist(Exception):
    pass
