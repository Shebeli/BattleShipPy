from datetime import datetime,  timedelta
from uuid import uuid4

from fastapi import HTTPException, status, APIRouter, Depends

from api.schemas.lobby import Lobby, LobbyIn, LobbyOut, LobbyGetList, LobbyGet
from api.auth.jwt import lobbies, get_user_from_header_token
from api.auth.utils import check_user_lobby
from api.models.user import User
from api.models.lobby import Lobby
from api.conf.settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

router = APIRouter()

@router.get("/get-lobbies/", response_model=LobbyGetList)
async def get_lobbies():
    return [lobby.to_dict() for lobby in lobbies]

@router.get("/get-lobby/{lobby_id}", response_model=LobbyGet)
async def get_lobby(lobby_id: lobby_id):
    for lobby in lobbies:
        if lobby.id == lobby_id:
            return lobby.to_dict()

@router.post("/create-lobby/", response_model=LobbyOut, status_code=status.HTTP_201_CREATED)
async def create_lobby(user: User = Depends(get_user_from_header_token)):
    check_user_lobby(user, lobbies)
    lobby = lobbies.create_and_add(user)
    return lobby.to_dict()

@router.post("/join-lobby/", response_model=LobbyOut)
async def join_lobby(lobby_input: LobbyIn, user: User = Depends(get_user_from_header_token)):
    check_user_lobby(user, lobbies)
    for lobby in lobbies:
        if lobby.uuid == lobby_input.uuid:
            if lobby.is_full:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Lobby is full!')
            lobby.add_player(user)
            return lobby.to_dict()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lobby not found')

@router.delete("/delete-lobby/{lobby_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_lobby(lobby_id: lobby_id, user: User = Depends(get_user_from_header_token)):
    lobby = lobbies.get(lobby_id)
    if not lobby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given lobby does not exist")
    if lobby.host != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only host can delete the lobby")
    lobbies.remove(lobby_id)
    return {"detail" : f"deleted lobby {lobby_id}"}

