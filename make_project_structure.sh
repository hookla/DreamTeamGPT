#!/bin/bash

# Create config directory and settings file
mkdir -p config
touch config/settings.py

# Create data directory and subdirectories
mkdir -p data/minutes
mkdir -p data/transcripts

# Create agents directory and Python files
mkdir -p agents
touch agents/__init__.py
touch agents/agent.py
touch agents/chairman.py
touch agents/executive.py
touch agents/secretary.py

# Create gpt directory and Python files
mkdir -p gpt
touch gpt/__init__.py
touch gpt/gpt_client.py

# Create utils directory and Python files
mkdir -p utils
touch utils/__init__.py
touch utils/token_counter.py

# Create tests directory and Python files
mkdir -p tests
touch tests/__init__.py
touch tests/test_agents.py
touch tests/test_gpt_client.py
touch tests/test_token_counter.py

# Create main.py, requirements.txt, and README.md in the root directory
touch main.py
touch requirements.txt
touch README.md

# Print directory structure
echo "Project structure created:"
find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
