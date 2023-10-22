from enum import Enum

from clients.base import AIClient
from clients.config import AIClientConfig
from clients.gpt_client import GPTClient


class AIClientType(str, Enum):
    ChatGPT = "ChatGPT"


def get_ai_client(client_type: AIClientType, config: AIClientConfig) -> AIClient:
    if client_type == AIClientType.ChatGPT:
        return GPTClient(config.api_key)
    else:
        raise ValueError(f"Unknown AI client type: {client_type}")
