from pydantic import BaseModel




class UserOut(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserOut

class UserIn(BaseModel):
    username: str
