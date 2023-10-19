from loguru import logger

from agents.agent import Agent
from agents.sme import SME


class Chairman(Agent):
    def __init__(self, name: str, executives: list):
        # Construct the user_prompt string with details of the executives
        exec_details = ""
        for executive_agent in executives:
            exec_details += f"{executive_agent.name}: expert in {executive_agent.expertise} and concerned about {', '.join(executive_agent.concerns)}.\n"

        user_prompt = (f"Your task is to decide who should speak next among meeting participates. Answer with only "
                       f"the name and nothing else.  Do not call on the same person too often.\nParticipants: {exec_details}")

        # Call the superclass constructor with the constructed user_prompt
        super().__init__(name, user_prompt)

        self.executives = executives

    def decide_if_meeting_over(self, transcript: list) -> bool:
        return False

    def decide_next_speaker(self, transcript_list: list) -> SME:
        transcript = " ".join(transcript_list)

        while True:

            next_speaker = self.query_gpt(transcript).strip().rstrip('.')
            logger.info(f"Chairman called speaker: {next_speaker}")

            next_executive = next((exec for exec in self.executives if exec.name == next_speaker), None)

            if next_executive is not None:
                return next_executive

            logger.info(f"{next_speaker} is not a valid exec...")
