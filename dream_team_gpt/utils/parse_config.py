from pathlib import Path
from typing import Dict, List, Any

import yaml
from loguru import logger
from pydantic import ValidationError

from dream_team_gpt.constants.sme_models import SMEConfig, SMETeam


def parse_yaml_config(file_path: Path) -> List[Dict[str, Any]]:
    """Parse SME configuration from a YAML file."""
    if not file_path:
        logger.warning("No config file provided")
        return []
        
    logger.info(f"Loading SMEs config file: {file_path}")
    
    try:
        # Load raw YAML data
        with open(file_path) as file:
            data = yaml.safe_load(file)
        
        # Validate using Pydantic model
        team = SMETeam.from_list(data)
        
        # Convert back to dict for backward compatibility
        return [member.model_dump() for member in team.members]
        
    except ValidationError as e:
        logger.error(f"Invalid SME configuration: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading SME configuration: {e}")
        raise