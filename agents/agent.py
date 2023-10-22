from textwrap import dedent

from clients.base import AIClient
from constants import NO_COMMENT

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
        client: AIClient,
        name: str,
        user_prompt: str,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ):
        self.name = name

        self.client = client
        self.client.common_instructions = system_prompt
        self.client.user_prompt = user_prompt

    def query_gpt(self, transcript: str) -> str:
        return self.client.query(transcript)
