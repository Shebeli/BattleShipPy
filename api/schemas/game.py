from pydantic import BaseModel, validator, root_validator
from typing import List, Optional, Tuple
 
from api.models.user import User

def validate_cordinate(cord: List[int]):
    if len(cord) != 2:
        raise ValueError("Cordinate only takes 2 integers")
    return cord

class ReadyGame(BaseModel):
    ready: bool

class StartGame(BaseModel):
    start: bool

class ReadyOut(BaseModel):
    id: int
    username: str
    ready: bool

class GameState(BaseModel):
    turn: str
    started: bool
    finished: bool
    winner: Optional[str] = None
class Map(BaseModel):
    map: List[List[int]] # enum

    class Config:
        schema_extra = {
            "example": {
                "map": [
                    [2, 2, 2, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 2, 2, 0, 0],
                    [2, 2, 2, 2, 0, 0, 2],
                    [0, 0, 0, 0, 0, 0, 2],
                    [0, 0, 0, 0, 0, 0, 2],
                ],
                "striked_ship": True
            }
        }

class SelectedCord(BaseModel):
    cordinate: List[int]

    _validate_cord = validator('cordinate', allow_reuse=True)(validate_cordinate)

    class Config:
        schema_extra = {
            "example": {
                "cordinate": [1, 2],
        }
    }

class SelectedCords(BaseModel):
    cordinates: List[List[int]]

    _validate_cord = validator('cordinates', allow_reuse=True, each_item=True)(validate_cordinate)

    class Config:
        schema_extra = {
            "example": {
                "cordinates": [
                    [2, 2],
                    [2, 3],
                    [2, 4]
                ]
            }
        }

class ShipOut(BaseModel):
    cordinates: List[List[int]]

    class Config:
        schema_extra = {
            "example": {
                "cordinates": [
                    [2, 2],
                    [2, 3],
                    [2, 4]
                ]
            }
        }    
class MoveShipCords(BaseModel):
    cordinate: List[int]
    cordinates: List[List[int]]

    class Config:
        schema_extra = {
            "example": {
                "cordinate": [1, 2],
                "cordinates": [
                    [2, 2],
                    [2, 3],
                    [2, 4]
                ]
            }
        }

    _validate_cord = validator('cordinate', allow_reuse=True)(validate_cordinate)
    _validate_cords = validator('cordinates', allow_reuse=True, each_item=True)(validate_cordinate)

