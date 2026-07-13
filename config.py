"""Configuration for the Nutrition agent.

This module defines a Pydantic settings class that provides
models and token-counting utilities.
"""

import logging
from functools import lru_cache

import tiktoken
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from strands.models.openai import OpenAIModel

logger = logging.getLogger(__name__)

# Approximate context windows, in tokens. Unlisted models fall back to
# the smallest window on record so budget checks stay conservative.
MODEL_CONTEXT_WINDOWS = {
    "gpt-5": 400_000,
    "gpt-5-mini": 400_000,
    "gpt-5-nano": 400_000,
    "gpt-4.1": 1_047_576,
    "gpt-4.1-mini": 1_047_576,
    "gpt-4.1-nano": 1_047_576,
    "gpt-4o": 128_000,
    "gpt-4o-mini": 128_000,
    "gpt-4-turbo": 128_000,
    "gpt-4-turbo-preview": 128_000,
    "gpt-4": 8_192,
    "gpt-4-32k": 32_768,
    "gpt-3.5-turbo": 16_385,
    "gpt-3.5-turbo-16k": 16_385,
}
DEFAULT_CONTEXT_WINDOW = 16_385
DEFAULT_ENCODING = "o200k_base"


class NutritionAgentConfig(BaseSettings):
    """Settings and helpers for the nutrition agent's API models."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    API_KEY: SecretStr
    AGENT_MODEL_NAME: str = Field(
        default="gpt-4o",
        description="Primary model used for responses",
    )
    AGENT_FALLBACK_MODEL_NAME: str = Field(
        default="gpt-4o-mini",
        description="Fallback model used if primary fails",
    )
    AGENT_MAX_TOKENS: int = 4096
    AGENT_TEMPERATURE: float = Field(
        default=0.3,
        le=1.0,
        ge=0.0,
        description=(
            "Controls randomness of the AI's responses. "
            "Lower values make output more deterministic."
        ),
    )
    TAVILY_API_KEY: SecretStr
    TOOL_MODEL_NAME: str = Field(
        default="gpt-4o",
        description="Primary model used for responses",
    )
    TOOL_FALLBACK_MODEL_NAME: str = Field(
        default="gpt-4o-mini",
        description="Fallback model used if primary fails",
    )

    def create_model(self, model_name: str) -> OpenAIModel:
        """Create an OpenAIModel instance with the given model name."""
        return OpenAIModel(
            client_args={"api_key": self.API_KEY.get_secret_value()},
            model_id=model_name,
            params={
                "temperature": self.AGENT_TEMPERATURE,
                "max_tokens": self.AGENT_MAX_TOKENS
            }
        )

    def get_fallback_model(self) -> OpenAIModel:
        """Retrieve the fallback model instance."""
        logger.info("Using fallback model: %s", self.AGENT_FALLBACK_MODEL_NAME)
        return self.create_model(self.AGENT_FALLBACK_MODEL_NAME)

    def get_primary_model(self) -> OpenAIModel:
        """Retrieve the primary model instance."""
        logger.info("Using primary model: %s", self.AGENT_MODEL_NAME)
        return self.create_model(self.AGENT_MODEL_NAME)

    def get_context_window(self, model_name: str) -> int:
        """
        Retrieve the context window size for a given model.

        Args:
            model_name (str): The name of the model to retrieve the context window for.
        """
        return MODEL_CONTEXT_WINDOWS.get(model_name, DEFAULT_CONTEXT_WINDOW)

    def check_prompt_fits(self, prompt: str, model_name: str) -> None:
        """Raise if the prompt would exceed the given model's context window."""
        token_count = self.count_tokens(prompt, model_name)
        available_tokens = self.get_context_window(model_name) - token_count

        if available_tokens <= 0:
            raise ValueError(
                f"Prompt exceeds context window of {model_name}."
            )


    @staticmethod
    @lru_cache
    def get_encoding(model_name: str) -> tiktoken.Encoding:
        """Return the token encoding for a given model name, falling back to a default."""
        try:
            return tiktoken.encoding_for_model(model_name)
        except KeyError:
            logger.warning(
                "No tiktoken encoding registered for model '%s', falling back to '%s'",
                model_name, DEFAULT_ENCODING
            )
            return tiktoken.get_encoding(DEFAULT_ENCODING)

    def count_tokens(self, prompt: str, model_name: str) -> int:
        """
        Count the number of tokens in a prompt based on the provided model.

        Args:
            prompt (str): The input prompt for the model.
            model_name (str): The name of the model to use.
        Returns:
            int: The length of the token list retrieved from the model.
        """
        encoding = self.get_encoding(model_name)
        return len(encoding.encode(prompt))


nutrition_config = NutritionAgentConfig()