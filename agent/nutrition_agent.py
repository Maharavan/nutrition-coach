from strands.agent import Agent
from agent.config import nutrition_config
from api.models import AgentResponse
import logging

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
            model=nutrition_config.get_model(),
            load_tools_from_directory=True
        )


    def __import_prompt(self) -> str:
        """Import the prompt from a markdown file."""

        with open("prompt.md", "r", encoding='utf-8') as file:
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
        response = self.agent.run(user_input)
        return AgentResponse(response=response)