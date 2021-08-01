from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends

from api.auth.jwt import create_access_token, get_user_from_header_token, users
from api.conf.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from api.models.user import User
from api.schemas.user import Token, UserIn, UserOut

router = APIRouter()


@router.post("/token", response_model=Token)
async def create_user_with_token(user: UserIn):
    user = users.create_and_add(user.username)
    access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': str(
        user.id), 'username': user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, user=user.to_dict())


@router.get("/token/test_header", response_model=UserOut)
async def test_token_header(user: User = Depends(get_user_from_header_token)):
    return user.to_dict()

@router.get("/user", response_model=List[UserOut])
async def get_users():
    return [user.to_dict() for user in users]
