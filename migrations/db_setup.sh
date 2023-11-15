#!/bin/bash

# Change to the directory of this script
cd "$(dirname "$0")"

# Run the Python script
python db_setup.py "$@"