from textwrap import dedent
from typing import Callable

from dream_team_gpt.agents.agent import Agent

USER_PROMPT_TEMPLATE = dedent(
    """\
    Adopt the persona of the {name}.\n
    Your expertise is {expertise}.\n
    Your concerns are {concerns}.\n
    You will be shown a transcript of a meeting. 
    You have been asked to speak by the meeting chairman. 
    Specifically, provide insights on {concerns} 
    based on the meeting transcript.\n
    Do not repeat points that have already been made
    """
)


class SME(Agent):
    def __init__(self, client_factory: Callable, name: str, expertise: str, concerns: list[str]):
        # Construct the user_prompt string
        user_prompt = USER_PROMPT_TEMPLATE.format(
            name=name, expertise=expertise, concerns=", ".join(concerns)
        )

        # Call the superclass constructor with the constructed user_prompt
        super().__init__(client_factory, name, user_prompt)
        self.expertise = expertise
        self.concerns = concerns
        self.spoken_count = 0

    def opinion(self, transcript: str) -> str:
        return self.query_gpt(transcript)
