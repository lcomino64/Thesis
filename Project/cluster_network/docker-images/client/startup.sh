#!/bin/bash
set -e

# Generate test files
/app/generate_testfiles.sh

# Start the wait-for-command script
python3 /app/wait-for-command.py