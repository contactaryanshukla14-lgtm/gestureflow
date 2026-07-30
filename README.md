# GestureFlow

Full-stack human-computer interaction project for gesture recognition using a React frontend, FastAPI backend, and MediaPipe/OpenCV-based data and training pipeline.

## Modules
- `frontend/`: webcam UI, prediction display, action history, settings, and dataset capture screen.
- `backend/`: FastAPI API for health, inference, logging, dataset summary, and training stubs.
- `ml/`: dataset capture, preprocessing, training, evaluation, and export scripts.
- `docs/`: PRD and architecture documentation.
- `docker/`: containerization files.

## Architecture Map
```mermaid
graph TD
    User([User]) -->|Webcam Video| Frontend[React/Vite UI]
    
    subgraph Client [Browser]
        Frontend
    end
    
    subgraph Server [FastAPI Backend]
        API[API Routes]
        Inference[ML Inference Service]
        DB[(SQLite Logs)]
    end
    
    Frontend -->|Send Frame/Data| API
    API --> Inference
    Inference -->|Gesture Label| API
    API -->|Save Log| DB
    API -.->|Action Command| OS[Operating System]
    API -->|Return Label| Frontend
    
    subgraph Pipeline [ML Pipeline]
        Capture[Dataset Capture] --> Preprocess[Data Preprocessing]
        Preprocess --> Train[Model Training]
        Train --> Export[Export Model Artifact]
    end
    
    Export -.->|Update| Inference
```

## Quick Start
To run the entire application (both frontend and backend) instantly, simply open your terminal in the project root and run:
```bash
bash start.sh
```
This will automatically launch the servers. Then, open [http://localhost:5173/](http://localhost:5173/) in your browser, allow webcam access, and start using gestures!
