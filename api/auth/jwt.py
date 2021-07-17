from datetime import datetime, timedelta
from typing import Optional, List, Dict, Set

from fastapi import HTTPException, status, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from jose import jwt, JWTError

from api.conf.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from api.models.user import UserSet
from api.models.lobby import LobbySet

security = HTTPBearer()
users = UserSet()
lobbies = LobbySet()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_from_header_token(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = int(payload.get('sub'))
        if user_id not in users.ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Username not found')
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Credentials are not valid???")
    return users.get(user_id) # user object

