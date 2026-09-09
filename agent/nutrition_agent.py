from pathlib import Path
import logging
from functools import lru_cache

from strands.agent import Agent
from config import nutrition_config
from api.models import AgentResponse
from agent.mem0_store import get_mem0_store 
logger = logging.getLogger(__name__)


class NutritionAgent:
    """Class representing a nutrition agent that provides nutritional advice based on user input."""
    def __init__(self, user_id: str):
        self.prompt = self.__import_prompt()
        self.mem0_store = get_mem0_store()
        self.memory_manager = self.mem0_store.get_memory_manager(user_id=user_id)
        self.agent = Agent(
            system_prompt=self.prompt,
            memory_manager=self.memory_manager,
            model=nutrition_config.get_primary_model(),
            load_tools_from_directory=True
        )


    def __import_prompt(self) -> str:
        """Import the prompt from a markdown file."""

        prompt_path = Path(__file__).parent / "agent_prompt.md"
        with open(prompt_path, "r", encoding='utf-8') as file:
            prompt = file.read()

        return prompt

    def get_nutrition_advice(self, user_input: str) -> AgentResponse:
        """
        Get nutritional advice based on user input.

        Args:
            user_input (str): The input from the user regarding nutrition.

        Returns:
            str: Nutritional advice or information.
        """
        try:
            response = self.agent(user_input)
        except Exception as e:
            logger.warning(
                "Primary model '%s' failed (%s), falling back to '%s'",
                nutrition_config.AGENT_MODEL_NAME, e, nutrition_config.AGENT_FALLBACK_MODEL_NAME
            )
            self.agent.model = nutrition_config.get_fallback_model()
            response = self.agent(user_input)
        return AgentResponse(response=str(response))

def get_nutrition_agent(user_id: str) -> NutritionAgent:
    """Get a cached instance of the NutritionAgent."""
    return NutritionAgent(user_id=user_id)