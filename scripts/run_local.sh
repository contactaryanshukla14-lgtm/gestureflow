#!/usr/bin/env bash
set -e
(cd backend && venv/Scripts/python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000) &
(cd frontend && npm install && npm run dev -- --host 0.0.0.0 --port 5173)
