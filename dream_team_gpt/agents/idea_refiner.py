from textwrap import dedent
from typing import Callable

from dream_team_gpt.agents.agent import Agent

REFINER_PROMPT = dedent(
    """\
    You are going to presented with an topic for discussion at a meeting. 
    Your task to think deeply and refine the topic presented and note obvious 
    high level constraints and considerations. 
    Your output will serve as an introduction to the meeting participants.
    """
)


class IdeaRefiner(Agent):
    def __init__(self, client_factory: Callable, name: str = "Refiner"):
        # Call the superclass constructor with the constructed user_prompt
        super().__init__(client_factory, name, REFINER_PROMPT)

    def refine_idea(self, idea: str) -> str:
        return self.query_gpt(idea)
