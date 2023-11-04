from dataclasses import dataclass, field
from pathlib import Path
from textwrap import dedent
import os

from loguru import logger

from dream_team_gpt.agents import SME, Chairman
from dream_team_gpt.agents.idea_refiner import IdeaRefiner
from dream_team_gpt.clients import AIClientConfig, AIClientType, Models, ai_client_factory
from dream_team_gpt.constants import DEFAULT_SME_DICT, NO_COMMENT
from dream_team_gpt.utils import parse_yaml_config, print_with_wrap


@dataclass
class Transcript(str):
    idea: str
    refined_idea: str = None
    opinions: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        opinions = "\n".join(opinion for opinion in self.opinions)
        return dedent(
            f"""\
            We are here to discuss the following idea:
            {self.refined_idea if self.refined_idea else self.idea}
            {opinions if opinions else ""}"""
        )

    def add_opinion(self, opinion: str) -> None:
        self.opinions.append(opinion)

    def __add__(self, other: str) -> "Transcript":
        if not isinstance(other, str):
            raise ValueError("Only can add string opinion to Transcript")

        self.add_opinion(other)
        return self


@dataclass
class Meeting:
    idea: str
    config: Path = None

    def __post_init__(self) -> None:
        """Create agents"""
        client_factory = ai_client_factory(
            AIClientConfig(
                client_type=AIClientType.ChatGPT,
                model=Models.GPT4,
                api_key=os.environ["openai.api_key"],
            )
        )
        if self.config:
            sme_dict = parse_yaml_config(self.config)
        else:
            sme_dict = DEFAULT_SME_DICT
        self.smes = [SME(client_factory=client_factory, **d) for d in sme_dict]
        self.chairman = Chairman(client_factory, self.smes)
        self.refiner = IdeaRefiner(client_factory, "Refiner")

    def run(self) -> None:
        """Run the meeting to discuss the idea"""
        transcript = Transcript(self.idea)
        print_with_wrap(transcript)
        refined_idea = self.refiner.refine_idea(self.idea)
        transcript.refined_idea = refined_idea
        print_with_wrap(refined_idea)
        while not self.chairman.decide_if_meeting_over(transcript):
            self.run_discussion_round(transcript)

    def run_discussion_round(self, transcript: str) -> None:
        logger.info("running next discussion round\n")
        speaker: SME = self.chairman.decide_next_speaker(transcript)
        opinion = speaker.opinion(transcript)
        print_with_wrap(f"\033[94m{speaker.name}\033[0m: {opinion}\n")
        if opinion.strip().rstrip(".").upper() != NO_COMMENT:
            transcript += opinion
