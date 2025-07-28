from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(data: LoginRequest):
    if data.username == "admin" and data.password == "1234":
        return {"access_token": "fake-jwt-token-for-admin", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")
