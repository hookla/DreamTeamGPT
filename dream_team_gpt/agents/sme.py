from collections.abc import Callable
from textwrap import dedent
from typing import Any

from dream_team_gpt.agents.agent import Agent
from dream_team_gpt.clients.base import AIClient

USER_PROMPT_TEMPLATE = dedent(
    """\
    Adopt the persona of the {name}.\n
    Your expertise is {expertise}.\n
    Your personality traits: {personality}.\n
    Your industry focus is {industry_focus}.\n
    Your primary concerns are {concerns}.\n
    You will be shown a transcript of a meeting about a fintech idea. 
    You have been asked to speak by the meeting chairman. 
    Provide insights on the idea based on your expertise, personality and concerns.
    Offer specific, actionable feedback related to your domain.
    Make 1-2 concrete suggestions for improvement.
    Do not repeat points that have already been made in the transcript.
    """
)


class SME(Agent):
    def __init__(
        self, 
        client_factory: Callable[..., AIClient], 
        name: str, 
        expertise: str, 
        concerns: list[str],
        personality: str = "Professional",
        industry_focus: str = "Financial services",
        **kwargs: Any
    ) -> None:
        # Construct the user_prompt string
        user_prompt = USER_PROMPT_TEMPLATE.format(
            name=name,
            expertise=expertise,
            personality=personality,
            industry_focus=industry_focus,
            concerns=", ".join(concerns),
        )

        # Call the superclass constructor with the constructed user_prompt
        super().__init__(client_factory, name, user_prompt)
        self.expertise = expertise
        self.concerns = concerns
        self.personality = personality
        self.industry_focus = industry_focus
        self.spoken_count = 0

    def opinion(self, transcript: str) -> str:
        self.spoken_count += 1
        return self.query_gpt(transcript)
