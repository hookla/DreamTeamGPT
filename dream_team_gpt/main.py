from pathlib import Path

import click
from dotenv import load_dotenv

from dream_team_gpt.config import settings
from dream_team_gpt.config.settings import AIClientType
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
@click.option(
    "--azure",
    is_flag=True,
    default=False,
    help="use Azure OpenAI instead of OpenAI API",
)
@click.option("-v", "--verbose", default=1, count=True)
def run_meeting(
    idea: str, config: Path | None = None, azure: bool = False, verbose: int = 1
) -> None:
    """Run a meeting with the team discussing the provided idea."""
    print(idea)
    # Load environment variables first
    load_dotenv()
    
    # Override settings with command line arguments
    if config:
        settings.sme_config_path = Path(config)
    if azure:
        settings.ai_client_type = AIClientType.AzureOpenAI
    
    # Configure logging based on verbosity
    configure_logging(verbose)

    # Create and run the meeting
    Meeting(idea).run()


if __name__ == "__main__":
    run_meeting()
