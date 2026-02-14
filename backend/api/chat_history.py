from fastapi import APIRouter, Depends, HTTPException
from backend.core.auth_utils import get_current_user
from backend.db.chat_repository import (
    get_conversation_messages,
    conversation_belongs_to_user,
)

router = APIRouter()


@router.get("/chat/history/{conversation_id}")
def get_chat_history(
    conversation_id: int,
    current_user=Depends(get_current_user),
):
    user_id = current_user.id

    # 🔒 Ownership check
    if not conversation_belongs_to_user(conversation_id, user_id):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this conversation",
        )

    messages = get_conversation_messages(conversation_id)

    return messages
