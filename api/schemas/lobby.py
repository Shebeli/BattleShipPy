from pydantic import BaseModel
from typing import Tuple
from uuid import uuid4

class LobbyGeneral(BaseModel):
    lobby_id: str
    host: int
    players: Tuple(int, int)
    has_started: bool = False
    is_full: bool = False

class LobbyOut(BaseModel):
    lobby_id: str
    host: int
    players: Tuple(int, int)


class LobbyIn(BaseModel):
    lobby_id: str


        