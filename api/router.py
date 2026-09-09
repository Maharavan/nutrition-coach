from fastapi import APIRouter, HTTPException, status

from agent.nutrition_agent import get_nutrition_agent
from api.models import AgentResponse, UserMessage
from logger_config import get_logger

logger = get_logger(__name__)
router = APIRouter()





@router.post("/chat")
async def chat_with_ai(message: UserMessage) -> AgentResponse:
    """
    Endpoint to handle chat interactions with the AI nutrition coach.
    
    Args:
        message: UserMessage containing user_id, message content, and timestamp
        
    Returns:
        AgentResponse with the nutrition coach's response
    """
    try:
        logger.info(f"Processing chat request from user {message.user_id}")
        nutrition_agent = get_nutrition_agent(user_id=message.user_id)
        logger.debug(f"Message: {message.message[:100]}...")  # Log first 100 chars
        
        response = nutrition_agent.get_nutrition_advice(message.message)
        
        logger.info(f"Chat request from user {message.user_id} processed successfully")
        return AgentResponse(response=response.response)
        
    except HTTPException:
        logger.warning(f"HTTP exception for user {message.user_id}")
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error while processing chat request from user {message.user_id}: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process your request. Please try again later.",
        )