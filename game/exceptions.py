from typing import Union, Any, Tuple


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
