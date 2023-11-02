from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv
import click

from dream_team_gpt.meeting import Meeting
from dream_team_gpt.utils import configure_logging


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
def run_meeting(idea: str, config: Path = None, verbose: int = 1) -> None:
    print(idea)
    configure_logging(verbose)
    load_dotenv()

    Meeting(idea, config).run()


if __name__ == "__main__":
    run_meeting()
