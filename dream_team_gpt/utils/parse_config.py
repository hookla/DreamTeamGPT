from pathlib import Path

from loguru import logger
import yaml


def parse_yaml_config(file_path: Path) -> list[dict]:
    logger.info(f"Loading SMEs config file: {file_path}")
    data = read_yaml(file_path)

    items = []
    for item in data:
        item_dict = {
            "name": item["name"],
            "expertise": item["expertise"],
            "concerns": item["concerns"],
        }
        items.append(item_dict)

    return items


def read_yaml(file_path: Path) -> list[dict]:
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data
