from pathlib import Path

from strands.agent import Agent
from config import nutrition_config
from strands.memory import MemoryManager
from api.models import AgentResponse
import logging

logger = logging.getLogger(__name__)

for _log in ["strands", "botocore", "boto3", "httpx", "urllib3",
             "strands.agent", "strands.tools", "strands.event_loop",
             "strands.models", "strands.experimental.bidi"]:
    logging.getLogger(_log).setLevel(logging.CRITICAL)

class NutritionAgent:
    """Class representing a nutrition agent that provides nutritional advice based on user input."""
    def __init__(self):
        self.prompt = self.__import_prompt()
        self.agent = Agent(
            system_prompt=self.prompt,
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