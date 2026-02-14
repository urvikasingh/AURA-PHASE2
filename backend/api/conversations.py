from fastapi import APIRouter, Depends, HTTPException, Query
from backend.core.auth_utils import get_current_user
from backend.db.chat_repository import (
    get_user_conversations,
    delete_conversation,
)

router = APIRouter(
    tags=["Conversations"]
)


@router.get("/conversations")
def list_conversations(
    domain: str | None = Query(
        None,
        description="Optional domain filter (academic, usp, etc.)"
    ),
    current_user=Depends(get_current_user),
):
    conversations = get_user_conversations(current_user.id)

    if domain:
        conversations = [
            c for c in conversations
            if c["domain"] == domain
        ]

    return conversations


@router.delete("/conversations/{conversation_id}")
def delete_conversation_endpoint(
    conversation_id: int,
    current_user=Depends(get_current_user),
):
    try:
        delete_conversation(
            conversation_id=conversation_id,
            user_id=current_user.id,
        )
        return {"status": "deleted"}
    except PermissionError:
        raise HTTPException(
            status_code=403,
            detail="Conversation does not belong to user",
        )
