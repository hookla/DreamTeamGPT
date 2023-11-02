from pathlib import Path
import os

from dotenv import load_dotenv
import click

from dream_team_gpt.agents import SME, Chairman
from dream_team_gpt.agents.idea_refiner import IdeaRefiner
from dream_team_gpt.clients import AIClientConfig, AIClientType, get_ai_client
from dream_team_gpt.constants import DEFAULT_SME_DICT, NO_COMMENT
from dream_team_gpt.utils import configure_logging, parse_yaml_config, print_with_wrap


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
    print(idea)
    configure_logging(verbose)
    load_dotenv()
    client = get_ai_client(
        AIClientType.ChatGPT,
        AIClientConfig(model="gpt-3.5-turbo", api_key=os.getenv("openai.api_key")),
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
