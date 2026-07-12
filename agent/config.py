from pydantic_settings import BaseSettings
from pydantic import Field
from strands.models.openai import OpenAIModel

class NutritionAgentConfig(BaseSettings):
    api_key: str 
    model_name: str = Field(default="gpt-4o", description="The name of the AI model to be used for generating responses")
    max_tokens: int = 4096
    temperature: float = Field(default=0.3, le=1.0, ge=0.0, description="Controls the randomness of the AI's responses. Lower values make the output more deterministic.")
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_model(self):
        return OpenAIModel(client_args={
            "api-key":self.api_key
            },            
            model_id=self.model_name,
            params={
                "temperature":self.temperature,
                "max_tokens":self.max_tokens
            }
        )

nutrition_config = NutritionAgentConfig()