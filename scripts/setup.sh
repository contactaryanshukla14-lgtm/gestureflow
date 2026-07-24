#!/usr/bin/env bash
set -e
cd backend
python -m venv venv
venv/Scripts/python -m pip install -r requirements.txt
cd ../frontend && npm install
