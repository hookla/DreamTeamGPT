from textwrap import dedent

from agents.agent import Agent
from clients import AIClient

REFINER_PROMPT = dedent(
    """\
    You are going to presented with an topic for discussion at a meeting. 
    Your task to think deeply and refine the topic presented and note obvious 
    high level constraints and considerations. 
    Your output will serve as an introduction to the meeting participants.
    """
)


class IdeaRefiner(Agent):
    def __init__(self, client: AIClient, name: str = "Refiner"):
        # Call the superclass constructor with the constructed user_prompt
        super().__init__(client, name, REFINER_PROMPT)

    def refine_idea(self, idea: str) -> str:
        return self.query_gpt(idea)
