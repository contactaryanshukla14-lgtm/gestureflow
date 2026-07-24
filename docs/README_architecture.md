# GestureFlow Architecture README

## Objective
GestureFlow is a human-computer interaction project that recognizes hand gestures from webcam input and maps them to software commands through a modular frontend, backend, and ML pipeline.

## End-to-End Flow
1. The frontend requests webcam access.
2. The live video stream is displayed in the browser.
3. The frontend sends a gesture sample or inference payload to the FastAPI backend.
4. The backend inference service predicts the gesture label.
5. The predicted label is translated into a UI action.
6. The event is logged in the database.
7. The frontend updates the prediction panel and interaction history.

## Training Flow
1. Capture labeled samples with the dataset utility.
2. Store samples under gesture-specific folders.
3. Split the dataset into train, validation, and test sets.
4. Run the training script to create the active model artifact.
5. Evaluate the model and export it to the archive path.

## Core Architectural Layers
- Presentation layer: React UI, webcam, prediction dashboard, controls.
- API layer: FastAPI routes for inference, health, logs, and dataset summary.
- Service layer: Gesture classification, action mapping, logging.
- ML layer: Dataset capture, preprocessing, training, evaluation, export.
- Persistence layer: SQLite tables for gesture logs and future model metadata.

## Folder Notes
- `frontend/` contains the interface and browser logic.
- `backend/` contains APIs, schemas, and persistence.
- `ml/` contains the computer-vision and training pipeline.
- `docs/` contains PRD and architecture documentation.
- `docker/` contains container files for packaging.

## Limitations
The included backend uses a deterministic demo inference service so the project can run immediately. Replace the inference service with a MediaPipe custom recognizer or landmark classifier for production-ready gesture recognition.
