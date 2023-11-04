from textwrap import dedent
from typing import Callable

from dream_team_gpt.constants import NO_COMMENT

DEFAULT_SYSTEM_PROMPT = dedent(
    f"""\
    Provide succinct, fact-based answers. Eliminate filler words and politeness. 
    Concentrate on delivering actionable insights and concrete solutions.
    Avoid vague or generic statements. Stick to the topic at hand. 
    If your response doesn't meet these standards, reply with the exact words '{NO_COMMENT}'
    """
)


class Agent:
    def __init__(
        self,
        client_factory: Callable,
        name: str,
        user_prompt: str,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ):
        self.name = name

        self.client = client_factory()
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.client.common_instructions = system_prompt
        self.client.user_prompt = user_prompt

    def query_gpt(self, transcript: str) -> str:
        self.client.system_instructions = self.system_prompt
        self.client.user_prompt = self.user_prompt
        return self.client.query(transcript)
