from pydantic import BaseModel
from typing import List

class Map(BaseModel):
    map: List[List[int]] # enum