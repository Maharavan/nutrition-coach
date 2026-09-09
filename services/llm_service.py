""""LLM service module for interacting with OpenAI models."""
import logging
from typing import List
import time

from openai import OpenAI, APIConnectionError, RateLimitError, AuthenticationError, BadRequestError
from pydantic import BaseModel, Field

from config import nutrition_config

logger = logging.getLogger(__name__)


class LLMResponse(BaseModel):
    """Result of a chat completion request."""

    content: str = Field(..., description="The generated text response")
    model: str = Field(..., description="The model that produced the response")


class LLMService:
    """Service class to interact with OpenAI's language models."""
    def __init__(self, models:List[str] | None = None):
        self.client = None
        try:
            self.client = OpenAI(api_key=nutrition_config.get_api_key())
        except ValueError:
            logger.warning(
                "OpenAI API key is not configured. LLM calls will fail until API_KEY is set in the environment."
            )
        self.models = models or [nutrition_config.TOOL_MODEL_NAME, nutrition_config.TOOL_FALLBACK_MODEL_NAME]

        self._check_model_instance(self.models)

    def _check_model_instance(self, models: List[str]) -> None:
        """Validate that models is a list of strings."""
        if not isinstance(models, list):
            raise TypeError("models must be a list of model names")

        if not all(isinstance(model, str) for model in models):
            raise TypeError("Each model must be a string")


    def get_available_models(self) -> List[str]:
        """Retrieve the configured primary and fallback tool models."""
        return self.models
    
    def _generate_response(self, user_prompt: str, system_prompt: str, model_name: str) -> LLMResponse:
        """Generate a response based on the provided prompt."""
        if self.client is None:
            raise RuntimeError(
                "OpenAI client is unavailable because API_KEY is not configured. Add the key to your .env file."
            )

        response = self.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role":"system","content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        generated_response = response.choices[0].message.content
        if generated_response is None:
            raise ValueError("No response generated")

        return LLMResponse(content=generated_response, model=model_name)

    def generate(self, user_prompt: str, system_prompt: str, attempts: int = 3) -> LLMResponse:
        """Generate a response, retrying across configured models on failure."""
        last_exception = None
        for model_name in self.get_available_models():
            for attempt in range(attempts):
                try:
                    return self._generate_response(user_prompt=user_prompt, system_prompt=system_prompt, model_name=model_name)
                except (APIConnectionError, RateLimitError) as e:
                    last_exception = e
                    logger.warning("Model %s failed with error: %s. Retrying...", model_name, e.__class__.__name__)
                    if attempt < attempts -1:
                        time.sleep(2**attempt)
                except (AuthenticationError, BadRequestError):
                    raise
                except Exception as e:
                    last_exception = e
                    logger.error("Model %s failed with error: %s. Trying next model.", model_name, e)
                
        raise RuntimeError("All models failed to run.") from last_exception
    
llm_service = LLMService()