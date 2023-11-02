from abc import ABC, abstractmethod


class AIClient(ABC):
    @abstractmethod
    def query(self, transcript: str):
        pass
