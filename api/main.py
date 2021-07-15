from typing import Optional

from fastapi import FastAPI, Header, Request
from pydantic import BaseModel
from api.endpoints import users


app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def root():
    return {"messageee": "Hellowwww"}

@app.get("/head")
async def read_items(request: Request, auth: Optional[str] = Header(None, alias='erejwirjwo')):
    print(auth[6:])
    return {"User-Ageeeent": auth, "request": request.headers}