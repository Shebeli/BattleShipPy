from .exceptions import NotValidChoiceError

from enum import Enum


class SquareStatus(Enum):
    EMPTY = 0
    MISSED = 1
    SHIP = 2
    HIT = 3

    @classmethod
    def values(cls):
        return [key.value for key in cls]

    @classmethod
    def validate(cls, state):
        if state not in cls.values():
            raise NotValidChoiceError


class Square:
    def __init__(self, state=0):
        self._state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        SquareStatus.validate(value)
        self._state = value

    def __str__(self):
        return SquareStatus(self.state).name  # 'eg. "EMPTY"'
