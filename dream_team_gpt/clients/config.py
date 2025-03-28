from dataclasses import dataclass
from typing import Optional

from pydantic import SecretStr

from dream_team_gpt.config.settings import AIClientType, ModelName


@dataclass
class AIClientConfig:
    """Configuration for AI clients."""
    
    client_type: AIClientType
    api_key: str
    model: Optional[str] = ModelName.GPT4O.value
    azure_endpoint: Optional[str] = None
    azure_deployment: Optional[str] = None
    
    @classmethod
    def from_settings(cls, settings):
        """Create a config instance from application settings."""
        return cls(
            client_type=settings.ai_client_type,
            api_key=settings.openai_api_key.get_secret_value(),
            model=settings.ai_model.value,
            azure_endpoint=settings.azure_openai_endpoint,
            azure_deployment=settings.azure_openai_deployment,
        )
