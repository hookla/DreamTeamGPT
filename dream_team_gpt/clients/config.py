from typing import Optional

from pydantic import BaseModel, Field, SecretStr, model_validator

from dream_team_gpt.config.settings import AIClientType, ModelName


class AIClientConfig(BaseModel):
    """Configuration for AI clients."""
    
    client_type: AIClientType = Field(..., description="Type of AI client")
    api_key: str = Field(..., description="API key for the service")
    model: str = Field(ModelName.GPT4O.value, description="Model name to use")
    azure_endpoint: Optional[str] = Field(None, description="Azure OpenAI endpoint")
    azure_deployment: Optional[str] = Field(None, description="Azure OpenAI deployment name")
    
    @model_validator(mode='after')
    def validate_azure_settings(self):
        """Validate Azure-specific settings."""
        if self.client_type == AIClientType.AzureOpenAI:
            if not self.azure_endpoint or not self.azure_deployment:
                missing = []
                if not self.azure_endpoint:
                    missing.append("azure_endpoint")
                if not self.azure_deployment:
                    missing.append("azure_deployment")
                raise ValueError(f"When using Azure OpenAI, {', '.join(missing)} must be provided")
        return self
    
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
