from collections.abc import Callable
from typing import Any

from .base import AIClient
from .config import AIClientConfig, AIClientType
from .gpt_client import GPTClient


def get_ai_client(config: AIClientConfig) -> AIClient:
    if config.client_type in (AIClientType.ChatGPT, AIClientType.AzureOpenAI):
        client = GPTClient(config.api_key, config.model)

        # Set Azure-specific config if needed
        if config.client_type == AIClientType.AzureOpenAI:
            import os

            os.environ["AZURE_OPENAI_ENDPOINT"] = config.azure_endpoint or ""
            os.environ["AZURE_OPENAI_DEPLOYMENT"] = config.azure_deployment or ""

        return client
    raise ValueError(f"Unknown AI client type: {config.client_type}")


def ai_client_factory(config: AIClientConfig) -> Callable[[Any], AIClient]:
    # Create a single client instance that will be reused
    client_instance = get_ai_client(config)
    return lambda _: client_instance


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

    def __init__(self, config: AIClientConfig) -> None:
        self.config = config

    def __call__(
        self,
        client_type: AIClientType | None = None,
        model: str | None = None,
    ) -> Callable[[Any], AIClient]:
        if client_type:
            self.config.client_type = client_type
        if model:
            self.config.model = model

        # Create a single client instance that will be reused
        client_instance = get_ai_client(self.config)
        return lambda _: client_instance
