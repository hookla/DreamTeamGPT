from dataclasses import dataclass


@dataclass
class AIClientConfig:
    api_key: str
    model: str | None
