from textwrap import dedent

from gpt.gpt_client import GPTClient


class Agent:
    def __init__(self, name: str, user_prompt: str):
        self.name = name
        self.common_instructions = dedent(
            """\
            For the duration of this conversation, provide raw, concise opinions 
            without any politeness or filler words. 
            Focus on progressing the solution in a tangible way. 
            Avoid generic statements and repetition of points already made. 
            Ensure all comments are directly relevant to the conversation. 
            If you cannot meet these criteria, respond with 'no comment.'
            """
        )
        self.gpt_client = GPTClient(self.common_instructions, user_prompt)

    def query_gpt(self, transcript: str) -> str:
        return self.gpt_client.query(transcript)
