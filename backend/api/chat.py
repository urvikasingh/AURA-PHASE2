from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.router.domain_router import route_message
from backend.core.auth_utils import get_current_user

router = APIRouter()


class ChatRequest(BaseModel):
    domain: str   # "usp", "academic", "legal", "medical"
    message: str


class ChatResponse(BaseModel):
    reply: str
    domain: str


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):
    # ✅ user_id comes from JWT, NOT from frontend
    user_id = current_user.id

    reply = route_message(
        domain=request.domain,
        message=request.message,
        user_id=user_id,
    )

    return {
        "reply": reply,
        "domain": request.domain,
    }
