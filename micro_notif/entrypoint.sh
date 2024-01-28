#!/usr/bin/env bash
set -e

# Add /app to PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Run the program
python micro_notif/main.py
