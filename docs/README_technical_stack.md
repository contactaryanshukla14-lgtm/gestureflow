# GestureFlow Technical Stack README

## Architectural Summary
GestureFlow uses a React frontend for user interaction, a FastAPI backend for APIs and orchestration, SQLite for lightweight persistence, and Python ML scripts for gesture dataset handling and model lifecycle management.

## Technology Stack
- Frontend: React, Vite, Axios, browser MediaDevices API.
- Backend: FastAPI, Uvicorn, Pydantic, SQLAlchemy.
- Database: SQLite for MVP logging and configuration.
- CV/ML: OpenCV, MediaPipe, NumPy, Pandas, scikit-learn.
- Packaging: Docker, shell scripts, ZIP archive.

## Database Notes
SQLite is used for the MVP because it is simple to run locally and sufficient for gesture logs, training metadata, and lightweight configuration. PostgreSQL can replace it later without major architectural changes.

## Component Responsibilities
- React UI: webcam view, controls, prediction card, dataset summary, event history.
- API router: health, inference, logs, training trigger, dataset summary.
- Gesture service: label inference, action mapping, logging operations.
- Dataset scripts: sample capture and split generation.
- Model scripts: training stub, evaluation stub, export pipeline.

## Library-Specific Rationale
- React: fast component-driven UI for dashboard-style interaction.
- Vite: lightweight local development and build flow.
- FastAPI: typed APIs and fast local backend setup.
- SQLAlchemy: ORM support for future schema growth.
- OpenCV: webcam capture and image operations.
- MediaPipe: hand landmark and gesture recognition pipeline extension point.
- scikit-learn / TensorFlow: suitable for classical or neural classifier upgrades.

## Upgrade Path
1. Replace demo inference with landmark extraction and custom model loading.
2. Add model registry and training-run tables.
3. Add frontend calibration and confidence-threshold controls.
4. Add Docker Compose execution for one-command startup.
