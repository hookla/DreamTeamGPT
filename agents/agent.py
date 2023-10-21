from textwrap import dedent

from gpt.gpt_client import GPTClient

DEFAULT_SYSTEM_PROMPT = dedent("""\
Provide succinct, fact-based answers. Eliminate filler words and politeness. 
Concentrate on delivering actionable insights and concrete solutions.
Avoid vague or generic statements. Stick to the topic at hand. 
If your response doesn't meet these standards, reply with the exact phrase 'no comment'
"""
)

class Agent:
    def __init__(self, name: str, user_prompt: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self.name = name
        self.gpt_client = GPTClient(system_prompt, user_prompt)

    def query_gpt(self, transcript: str) -> str:
        return self.gpt_client.query(transcript)
