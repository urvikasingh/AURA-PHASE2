from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.auth_utils import hash_password, verify_password
from backend.db.user_repository import create_user, get_user_by_email

router = APIRouter()


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(data: SignupRequest):
    password_hash = hash_password(data.password)
    user_id = create_user(data.email, password_hash)
    return {"user_id": user_id}


@router.post("/login")
def login(data: LoginRequest):
    user = get_user_by_email(data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id, password_hash = user

    if not verify_password(data.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"user_id": user_id}
