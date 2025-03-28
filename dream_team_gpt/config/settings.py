from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AIClientType(str, Enum):
    """Type of AI client to use."""
    
    ChatGPT = "ChatGPT"
    AzureOpenAI = "AzureOpenAI"


class ModelName(str, Enum):
    """Known LLM model types."""
    
    GPT3 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    GPT4O = "gpt-4o"


class Settings(BaseSettings):
    """Application settings that can be configured via environment variables."""
    
    # API Settings
    openai_api_key: SecretStr = Field(..., description="OpenAI API key")
    ai_client_type: AIClientType = Field(
        default=AIClientType.ChatGPT,
        description="Type of AI client to use"
    )
    ai_model: ModelName = Field(
        default=ModelName.GPT4O, 
        description="AI model to use"
    )
    
    # Azure-specific settings
    azure_openai_endpoint: Optional[str] = Field(
        default=None,
        description="Azure OpenAI endpoint (only needed for Azure)"
    )
    azure_openai_deployment: Optional[str] = Field(
        default=None, 
        description="Azure OpenAI deployment name (only needed for Azure)"
    )
    
    # Application settings
    log_level: str = Field(
        default="INFO", 
        description="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    sme_config_path: Optional[Path] = Field(
        default=None,
        description="Path to the YAML file with team personalities"
    )
    
    # Validate Azure settings when using Azure
    @field_validator('azure_openai_endpoint', 'azure_openai_deployment')
    def validate_azure_settings(cls, v: Optional[str], info: Dict[str, Any]) -> Optional[str]:
        values = info.data
        if values.get('ai_client_type') == AIClientType.AzureOpenAI and not v:
            field_name = info.field_name
            raise ValueError(f"{field_name} must be provided when using Azure OpenAI")
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


# Create a global settings instance
settings = Settings()