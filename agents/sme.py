from agents.agent import Agent


class SME(Agent):
    def __init__(self, name: str, expertise: str, concerns: list[str]):
        # Construct the user_prompt string
        user_prompt_list = [
            f"Adopt the persona of the {name}.",
            f"Your expertise is {expertise}.",
            f"Your concerns are {', '.join(concerns)}.",
            f"You will be shown a transacript of a meeting.  You have been asked to speak by the meeting chairman.  Specifically, provide insights on {', '.join(concerns)} based on the meeting transcript. "
            "Do not repeat points that have already been made.",
        ]
        user_prompt = " ".join(user_prompt_list)

        # Call the superclass constructor with the constructed user_prompt
        super().__init__(name, user_prompt)
        self.expertise = expertise
        self.concerns = concerns
        self.spoken_count = 0

    def opinion(self, transcript_list: list[str]) -> str:
        transcript = " ".join(transcript_list)
        return self.query_gpt(transcript)
