from textwrap import dedent

from gpt.gpt_client import GPTClient


class Agent:
    def __init__(self, name: str, user_prompt: str):
        self.name = name
        
        self.common_instructions = dedent(
        """\
        Provide succinct, fact-based answers. Eliminate filler words and politeness. 
        Concentrate on delivering actionable insights and concrete solutions.
        Avoid vague or generic statements. Stick to the topic at hand. 
        If the query doesn't meet these standards, reply with 'no comment.'
        """
        )

        self.gpt_client = GPTClient(self.common_instructions, user_prompt)

    def query_gpt(self, transcript: str) -> str:
        return self.gpt_client.query(transcript)
