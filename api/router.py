from fastapi import APIRouter

from api.models import UserMessage

router = APIRouter()

@router.post("/chat")
async def chat_with_ai(message: UserMessage):
    """Endpoint to handle chat interactions with the AI nutrition coach."""
    # Logic for handling chat interactions would go here
    return {"message": "Chat endpoint is under construction."}

