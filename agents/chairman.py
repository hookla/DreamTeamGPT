from loguru import logger

from agents.agent import Agent
from agents.sme import SME
from clients.base import AIClient


class Chairman(Agent):
    def __init__(self, client: AIClient, executives: list[SME], name: str = "Chairman"):
        # Construct the user_prompt string with details of the executives
        self.user_prompt = self.update_user_prompt(executives)

        system_prompt = f"Answer with only the name and nothing else."

        # Call the superclass constructor with the constructed user_prompt
        super().__init__(client, name, self.user_prompt, system_prompt)

        self.executives = executives

    def update_user_prompt(self, SMEs: list[SME]) -> str:
        frequency_info_list = []
        for sme in SMEs:
            frequency_info_list.append(
                f"{sme.name}: expertise: {sme.expertise}. "
                f"concerns: {', '.join(sme.concerns)}. spoken count: {sme.spoken_count}.\n"
            )

        return (
            f"Your task is to read the transcript and decide who should speak next. "
            f"Do not choose the same person all of the time.\n"
            f"Participants:\n{''.join(frequency_info_list)} "
        )

    def decide_if_meeting_over(self, transcript: list) -> bool:
        return False

    def decide_next_speaker(self, transcript_list: list[str]) -> SME:
        transcript = " ".join(transcript_list)

        while True:
            next_speaker = self.query_gpt(transcript).strip().rstrip(".")
            logger.info(f"Chairman called speaker: {next_speaker}")

            next_executive = next(
                (exec for exec in self.executives if exec.name == next_speaker), None
            )

            if next_executive is not None:
                next_executive.spoken_count += 1  # Update the frequency count
                self.user_prompt = self.update_user_prompt(self.executives)
                self.client.user_prompt = self.user_prompt
                return next_executive

            logger.info(f"{next_speaker} is not a valid exec...")
