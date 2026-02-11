from fastapi import APIRouter
from pydantic import BaseModel
from backend.router.domain_router import route_message

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: int
    domain: str   # "usp", "academic", "legal", "medical"
    message: str


class ChatResponse(BaseModel):
    reply: str
    domain: str


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    reply = route_message(
        user_id=request.user_id,
        domain=request.domain,
        message=request.message
    )

    return {
        "reply": reply,
        "domain": request.domain
    }
