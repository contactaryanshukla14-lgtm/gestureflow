#!/usr/bin/env bash

# Convenience script to start the application
echo "Starting GestureFlow..."

# Ensure we are in the project root directory
cd "$(dirname "$0")"

# Execute the main run script
bash scripts/run_local.sh
