from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

@router.post("/register")
async def register(user: UserCreate):
    # placeholder: save user to DB; return stubbed response for now
    return {"msg": "user registered (stub)", "email": user.email}

@router.post("/login")
async def login():
    # placeholder: issue JWT in later steps
    return {"access_token": "stub-token", "token_type": "bearer"}