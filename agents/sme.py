from textwrap import dedent

from agents.agent import Agent
from clients.base import AIClient

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
    def __init__(
        self, client: AIClient, name: str, expertise: str, concerns: list[str]
    ):
        # Construct the user_prompt string
        user_prompt = USER_PROMPT_TEMPLATE.format(
            name=name, expertise=expertise, concerns=", ".join(concerns)
        )

        # Call the superclass constructor with the constructed user_prompt
        super().__init__(client, name, user_prompt)
        self.expertise = expertise
        self.concerns = concerns
        self.spoken_count = 0

    def opinion(self, transcript_list: list[str]) -> str:
        transcript = " ".join(transcript_list)
        return self.query_gpt(transcript)
