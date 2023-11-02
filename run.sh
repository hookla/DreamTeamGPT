#!/bin/bash

# Append "mydream_team_gpt" to PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Change directory to "myapp" subdir
cd dream_team_gpt || exit

# Run the main.py with command-line arguments
python main.py "$@"
