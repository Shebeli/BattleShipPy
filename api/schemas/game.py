from pydantic import BaseModel, validators
from typing import List, Optional

class Map(BaseModel):
    map: List[List[int]] # enum
    striked_ship: Optional[bool] = False

class SelectSquare(BaseModel):
    cordinate: List[int]

    @validators('cordinate')
    def cordinate_must_be_valid(cls, v):
        if len(v) != 2:
            raise ValueError("Cordinate only takes 2 integers")
        return v

class SelectedSquares(BaseModel):
    Cordinates: List[SelectSquare]

