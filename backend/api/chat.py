from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from backend.router.domain_router import route_message
from backend.core.auth_utils import get_current_user
from backend.db.chat_repository import (
    create_conversation,
    save_message,
    update_conversation_timestamp,
)

router = APIRouter()


class ChatRequest(BaseModel):
    domain: str                 # "usp", "academic", "legal", "medical"
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    reply: str
    domain: str
    conversation_id: int


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):
    # ✅ user_id comes from JWT
    user_id = current_user.id

    # 1️⃣ Create or reuse conversation
    if request.conversation_id is None:
        conversation_id = create_conversation(
            user_id=user_id,
            domain=request.domain,
        )
    else:
        conversation_id = request.conversation_id
        update_conversation_timestamp(conversation_id)

    # 2️⃣ Save user message
    save_message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=request.message,
    )

    # 3️⃣ Route message to domain logic
    reply = route_message(
        domain=request.domain,
        message=request.message,
        user_id=user_id,
        conversation_id=conversation_id,

    )

    # 4️⃣ Save assistant reply
    save_message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="assistant",
        content=reply,
    )

    return {
        "reply": reply,
        "domain": request.domain,
        "conversation_id": conversation_id,
    }
