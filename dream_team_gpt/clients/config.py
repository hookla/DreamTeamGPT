from dataclasses import dataclass
from enum import Enum

from .gpt_client import Models


class AIClientType(str, Enum):
    ChatGPT = "ChatGPT"
    AzureOpenAI = "AzureOpenAI"


@dataclass
class AIClientConfig:
    client_type: AIClientType
    api_key: str
    model: str | None = Models.GPT4O
    azure_endpoint: str | None = None
    azure_deployment: str | None = None
