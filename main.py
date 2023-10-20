from pathlib import Path

import click
from loguru import logger

from agents.chairman import Chairman
from agents.sme import SME
from utils.parse_config import parse_yaml_config
from utils.print_with_wrap import print_with_wrap

logger.disable(__name__)

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

    transcript = [idea]

    print(transcript)
    while not chairman.decide_if_meeting_over(transcript):
        speaker: SME = chairman.decide_next_speaker(transcript)

        opinion = speaker.opinion(transcript)

        print_with_wrap(f"\033[94m{speaker.name}\033[0m: {opinion}")


if __name__ == "__main__":
    main()
