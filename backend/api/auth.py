from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.auth_utils import hash_password, verify_password
from backend.db.user_repository import create_user, get_user_by_email
from backend.core.auth_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


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

    if user_id is None:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

    return {"user_id": user_id}


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    user_id, password_hash = user

    if not verify_password(form_data.password, password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token({"sub": str(user_id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

