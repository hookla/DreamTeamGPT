from pathlib import Path

import click
from loguru import logger

from agents.chairman import Chairman
from agents.idea_refiner import IdeaRefiner
from agents.sme import SME
from constants import NO_COMMENT
from utils.parse_config import parse_yaml_config
from utils.print_with_wrap import print_with_wrap
import logger_config

# typical C-suite of executives
DEFAULT_SME_DICT = (
    {
        "name": "CEO",
        "expertise": "Corporate Strategy",
        "concerns": ["Market Entry", "Competitive Positioning"],
    },
    {
        "name": "CFO",
        "expertise": "Financial Products",
        "concerns": ["Rate Management", "Regulatory Compliance"],
    },
    {
        "name": "COO",
        "expertise": "Operational Efficiency",
        "concerns": ["Scalability", "Cost Optimization"],
    },
    {
        "name": "CMO",
        "expertise": "Customer Acquisition",
        "concerns": ["Target Market", "Onboarding Experience"],
    },
    {
        "name": "CTO",
        "expertise": "Technical Infrastructure",
        "concerns": ["Data Security", "System Integration"],
    },
    {
        "name": "CRO",
        "expertise": "Risk Management",
        "concerns": ["Fraud Detection", "Compliance"],
    },
    {
        "name": "CCO",
        "expertise": "Customer Experience",
        "concerns": ["UX/UI Design", "Customer Support"],
    },
    {
        "name": "CPO",
        "expertise": "Product Management",
        "concerns": ["Feature Rollout", "Customer Feedback"],
    },
)


@click.command()
@click.option(
    "--idea",
    "-i",
    type=str,
    required=True,
    help="your idea for the team to discuss. Please use double quotes",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    default=None,
    help="yaml file with team personalities details",
)
def main(idea: tuple[str], config: Path = None):
    if config:
        sme_dict = parse_yaml_config(config)
    else:
        sme_dict = DEFAULT_SME_DICT

    smes = [SME(**d) for d in sme_dict]

    chairman = Chairman("Chairman", smes)
    refiner = IdeaRefiner("Refiner")

    transcript = ["<TRANSCRIPT OF ONGOING MEETING>", ".", "We are here to discuss this idea:", idea, "."]

    print_with_wrap("\n".join(transcript))

    refined_idea = refiner.refine_idea(idea)
    transcript.append(refined_idea)
    print_with_wrap(refined_idea)
    print()

    while not chairman.decide_if_meeting_over(transcript):
        speaker: SME = chairman.decide_next_speaker(transcript)

        opinion = speaker.opinion(transcript)

        print_with_wrap(f"\033[94m{speaker.name}\033[0m: {opinion}")
        print()
        if opinion.strip().rstrip(".").upper() != NO_COMMENT:
            transcript.append(opinion)


if __name__ == "__main__":
    main()
