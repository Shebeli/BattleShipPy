from pydantic import BaseModel
from typing import List
from uuid import uuid4

from api.schemas.user import UserIn, UserOut
class LobbyGet(BaseModel):
    uuid: str
    host: UserOut
    players: List[UserOut]
    has_started: bool = False
    is_full: bool = False
class LobbyGetList(BaseModel):
    lobbies: List[LobbyGet]

class LobbyOut(BaseModel):
    id: int
    uuid: str
    host: UserOut
    players: List[UserOut]


class LobbyIn(BaseModel):
    uuid: str


        