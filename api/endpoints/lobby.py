from datetime import datetime,  timedelta
from uuid import uuid4

from fastapi import HTTPException, status, APIRouter, Depends

from api.schemas.lobby import Lobby, LobbyIn, LobbyOut
from api.auth.jwt import create_access_token, get_user_from_header_token, get_used_id_from_token, UsersList, add_user, Lobbies
from api.conf.settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

router = APIRouter()

@router.post("/create-lobby/", response_model=LobbyOut)
def create_lobby(user_id: Depends(get_used_id_from_token)):
    if any((users[0]==user_id or users[1]==user_id for users in Lobbies.values())):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already in a lobby.")
    lobby_id = uuid4().hex[:10]
    Lobbies[lobby_id] = set().add(user_id)
    