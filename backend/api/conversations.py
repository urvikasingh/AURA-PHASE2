from fastapi import APIRouter, Depends, Query
from backend.core.auth_utils import get_current_user
from backend.db.chat_repository import get_user_conversations

router = APIRouter()


@router.get("/conversations")
def list_conversations(
    domain: str = Query(..., description="Domain like academic or usp"),
    current_user=Depends(get_current_user),
):
    user_id = current_user.id

    conversations = get_user_conversations(user_id)

    # 🔒 Filter by domain
    filtered = [
        c for c in conversations
        if c["domain"] == domain
    ]

    return filtered
