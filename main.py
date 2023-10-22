import os
from pathlib import Path

import click
from dotenv import load_dotenv

from agents.chairman import Chairman
from agents.idea_refiner import IdeaRefiner
from agents.sme import SME
from clients import AIClientConfig, AIClientType, get_ai_client
from constants import NO_COMMENT
from utils.logging import configure_logging
from utils.parse_config import parse_yaml_config
from utils.print_with_wrap import print_with_wrap

load_dotenv()

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
@click.option("-v", "--verbose", default=1, count=True)
def main(idea: str, config: Path = None, verbose: int = 1):
    configure_logging(verbose)
    load_dotenv()
    client = get_ai_client(
        AIClientType.ChatGPT, AIClientConfig(api_key=os.getenv("openai.api_key"))
    )
    if config:
        sme_dict = parse_yaml_config(config)
    else:
        sme_dict = DEFAULT_SME_DICT

    smes = [SME(client=client, **d) for d in sme_dict]

    chairman = Chairman(client, smes)

    refiner = IdeaRefiner(client, "Refiner")

    transcript = [
        "<TRANSCRIPT OF ONGOING MEETING>",
        ".",
        "We are here to discuss this idea:",
        idea,
        ".",
    ]

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
