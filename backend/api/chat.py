from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import time

from backend.router.domain_router import route_message
from backend.core.auth_utils import get_current_user
from backend.db.chat_repository import (
    create_conversation,
    save_message,
    update_conversation_timestamp,
)
from backend.db.experiment_repository import log_experiment
from backend.memory.memory_gate import was_memory_triggered

router = APIRouter()


class ChatRequest(BaseModel):
    domain: str
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

    # ⏱️ START TIMER
    start_time = time.perf_counter()

    # 3️⃣ Route message to domain logic
    reply = route_message(
        domain=request.domain,
        message=request.message,
        user_id=user_id,
        conversation_id=conversation_id,
    )

    # ⏱️ END TIMER
    latency_ms = (time.perf_counter() - start_time) * 1000

    # 4️⃣ Save assistant reply
    save_message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="assistant",
        content=reply,
    )

    # 🧪 RESEARCH LOG (does NOT affect response)
    log_experiment(
        user_id=user_id,
        conversation_id=conversation_id,
        domain=request.domain,
        memory_triggered=was_memory_triggered(),
        latency_ms=latency_ms,
        input_length=len(request.message),
        output_length=len(reply),
    )

    return {
        "reply": reply,
        "domain": request.domain,
        "conversation_id": conversation_id,
    }
