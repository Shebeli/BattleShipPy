from pydantic import BaseModel
from typing import List

from api.schemas.game import ReadyOut
from api.schemas.user import UserOut


class LobbyOut(BaseModel):
    id: int
    uuid: str
    host: UserOut
    players: List[ReadyOut]
    has_started: bool = False
    is_full: bool = False


class LobbyIn(BaseModel):
    uuid: str
