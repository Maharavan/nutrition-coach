from fastapi import APIRouter, HTTPException
from agent.nutrition_agent import get_nutrition_agent
from api.models import UserMessage

router = APIRouter()

nutrition_agent = get_nutrition_agent()

@router.post("/chat")
async def chat_with_ai(message: UserMessage):
    """Endpoint to handle chat interactions with the AI nutrition coach."""

    # Logic for handling chat interactions would go here
    try:
        response = nutrition_agent.get_nutrition_advice(message.content)
        return {"message": response.response}
    except HTTPException:
        return {"message": "An error occurred while processing your request."}
    except Exception as e:
        return {"message": f"Unexpected error: {str(e)}"}