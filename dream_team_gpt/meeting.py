from pathlib import Path
from textwrap import dedent
from typing import List, Optional

from loguru import logger
from pydantic import BaseModel, Field, field_validator

from dream_team_gpt.agents import SME, Chairman
from dream_team_gpt.agents.idea_refiner import IdeaRefiner
from dream_team_gpt.clients import AIClientConfig, ai_client_factory
from dream_team_gpt.config import settings
from dream_team_gpt.constants import DEFAULT_SME_DICT, NO_COMMENT
from dream_team_gpt.utils import parse_yaml_config, print_with_wrap


class Transcript(BaseModel):
    """Meeting transcript containing the idea and all opinions."""
    
    idea: str = Field(..., description="The original idea being discussed")
    refined_idea: Optional[str] = Field(None, description="The refined version of the idea")
    opinions: List[str] = Field(default_factory=list, description="List of opinions from executives")
    
    def __str__(self) -> str:
        """Format the transcript for display."""
        opinions = "\n".join(opinion for opinion in self.opinions)
        return dedent(
            f"""\
            We are here to discuss the following idea:
            {self.refined_idea if self.refined_idea else self.idea}
            {opinions if opinions else ""}""",
        )

    def add_opinion(self, opinion: str) -> None:
        """Add an opinion to the transcript."""
        if not opinion or not isinstance(opinion, str):
            return
        self.opinions.append(opinion)

    def __add__(self, other: str) -> "Transcript":
        """Support adding string opinions with the + operator."""
        self.add_opinion(other)
        return self
        
    model_config = {
        "arbitrary_types_allowed": True
    }


class Meeting(BaseModel):
    """A meeting with executives to discuss an idea."""
    
    idea: str = Field(..., description="The idea to discuss")
    smes: List[SME] = Field(default_factory=list, description="Subject matter experts in the meeting")
    chairman: Optional[Chairman] = Field(None, description="Meeting chairman/facilitator")
    refiner: Optional[IdeaRefiner] = Field(None, description="Idea refiner agent")
    
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    def model_post_init(self, __context) -> None:
        """Initialize agents using application settings."""
        # Configure the client
        client_config = AIClientConfig.from_settings(settings)

        # Create client factory
        client_factory = ai_client_factory(client_config)

        # Initialize agents with the configured client
        sme_dict = parse_yaml_config(settings.sme_config_path) if settings.sme_config_path else DEFAULT_SME_DICT

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

    def run_discussion_round(self, transcript: Transcript) -> None:
        logger.info("running next discussion round\n")
        speaker: SME = self.chairman.decide_next_speaker(transcript)
        opinion = speaker.opinion(transcript)
        print_with_wrap(f"\033[94m{speaker.name}\033[0m: {opinion}\n")
        if opinion.strip().rstrip(".").upper() != NO_COMMENT:
            transcript.add_opinion(f"{speaker.name}: {opinion}")
