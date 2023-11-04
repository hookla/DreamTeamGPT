from dataclasses import dataclass
from enum import Enum

from .gpt_client import Models


class AIClientType(str, Enum):
    ChatGPT = "ChatGPT"


@dataclass
class AIClientConfig:
    client_type: AIClientType
    api_key: str
    model: Models | None
