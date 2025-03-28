#!/bin/bash

# Append project root to PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Run the main.py with Poetry
poetry run python dream_team_gpt/main.py "$@"
