from fastapi import FastAPI
from backend.api.chat import router as chat_router
from backend.api import auth

app = FastAPI(title="AURA PHASE 2")

# Auth routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Chat routes
app.include_router(chat_router, tags=["Chat"])

@app.get("/")
def root():
    return {"message": "LLM Platform API is live"}

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "message": "Backend is running"
    }
