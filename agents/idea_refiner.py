from loguru import logger

from agents.agent import Agent
from agents.sme import SME


class IdeaRefiner(Agent):
    def __init__(self, name: str):
        # Construct the user_prompt string with details of the executives

        self.user_prompt = "You are going to presented with an topic for discussion at a meeting.  Your task to think deeply and refine the topic presented and note obvious high level constraints and considerations.  Your output will serve as an introduction to the meeting participants."


        # Call the superclass constructor with the constructed user_prompt
        super().__init__(name, self.user_prompt)

    def refine_idea(self, idea: str) -> str:
        return self.query_gpt(idea)
