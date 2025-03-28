from dream_team_gpt.agents.agent import Agent


class Secretary(Agent):
    def take_minutes(self, _minutes: list, _transcript: list) -> str:
        return "Example Minutes"
