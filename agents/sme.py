from agents.agent import Agent

class SME(Agent):

    def __init__(self, name: str, expertise: str, concerns: list[str]):
        # Construct the user_prompt string
        user_prompt_list = [
            f"Adopt the persona of the {expertise}.",
            f"Your concerns are {', '.join(concerns)}.",
            "You should aim to provide technical insights that align with these areas of expertise and concerns."
        ]
        user_prompt = " ".join(user_prompt_list)

        # Call the superclass constructor with the constructed user_prompt
        super().__init__(name, user_prompt)
        self.expertise = expertise
        self.concerns = concerns

    def opinion(self, transcript_list: list) -> str:
        transcript = " ".join(transcript_list)
        return self.query_gpt(transcript)
