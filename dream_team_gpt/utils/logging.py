import sys

from loguru import logger


def configure_logging(verbose: int = 0) -> None:
    logging_levels = {0: "ERROR", 1: "INFO", 2: "DEBUG"}
    logger.remove(0)
    logger.add(sys.stdout, level=logging_levels.get(verbose))
    logger.add("dream_team_gpt.log", level="DEBUG")
