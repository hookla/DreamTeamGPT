from pathlib import Path
from typing import Any

import yaml
from loguru import logger


def parse_yaml_config(file_path: Path) -> list[dict[str, Any]]:
    logger.info(f"Loading SMEs config file: {file_path}")
    data = read_yaml(file_path)

    items: list[dict[str, Any]] = []
    for item in data:
        item_dict = {
            "name": item["name"],
            "expertise": item["expertise"],
            "concerns": item["concerns"],
        }
        items.append(item_dict)

    return items


def read_yaml(file_path: Path) -> list[dict[str, Any]]:
    with open(file_path) as file:
        return yaml.safe_load(file)
