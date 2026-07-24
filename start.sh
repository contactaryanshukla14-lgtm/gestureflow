#!/usr/bin/env bash

# Convenience script to start the application
echo "Starting GestureFlow..."

# Ensure we are in the project root directory
cd "$(dirname "$0")"

# Check if the backend virtual environment exists. If not, run setup first.
if [ ! -d "backend/venv" ]; then
    echo "First time setup detected. Installing dependencies..."
    bash scripts/setup.sh
fi

# Install root dependencies (concurrently)
if [ ! -d "node_modules" ]; then
    npm install
fi

# Execute via npm start
npm start
