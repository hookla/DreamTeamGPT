from agents.agent import Agent


class Executive(Agent):
    def __init__(self, name: str, expertise: str, concerns: list[str]):
        super().__init__(name)
        self.expertise = expertise
        self.concerns = concerns

    def opinion(self, minutes_list: list, transcript_list: list) -> str:
        minutes = " ".join(minutes_list)
        transcript = " ".join(transcript_list)
        prompt = f"Adopt the persona of the {self.expertise}. Your concerns are {self.concerns}. Contribute to this conversation: Transcript Tail: {transcript}"
        return self.query_gpt(prompt, 100)
