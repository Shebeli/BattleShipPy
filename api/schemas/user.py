from pydantic import BaseModel
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserOut(BaseModel):
    id: int
    username: str
class UserIn(BaseModel):
    username: str 
