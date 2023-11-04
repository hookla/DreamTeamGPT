from dataclasses import dataclass
from typing import Any, Callable

from .base import AIClient
from .config import AIClientConfig, AIClientType
from .gpt_client import GPTClient, Models


def get_ai_client(config: AIClientConfig) -> AIClient:
    if config.client_type == AIClientType.ChatGPT:
        return GPTClient(config.api_key)
    else:
        raise ValueError(f"Unknown AI client type: {config.client_type}")


def ai_client_factory(config: AIClientConfig) -> Callable[[Any], AIClient]:
    return lambda _: get_ai_client(config)


@dataclass
class AIClientFactory:
    """Callable factory for AIClient.

    Usage:
    factory = AIClientFactory(config=AIClientConfig(...))
    Agent(factory)

    or

    factory.config.client_type=<AIClientType>
    factory.config.model=<Models>
    Agent(factory)

    or update these config params in Agent on calling the factory:

    factory(client_type=<AIClientType>,model=<Models>)

    """

    config: AIClientConfig

    def __call__(
        self, client_type: AIClientType = None, model: Models = None
    ) -> Callable[[Any], AIClient]:
        if client_type:
            self.config.client_type = client_type
        if model:
            self.config.model = model

        return lambda _: get_ai_client(self.config)
