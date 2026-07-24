from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import Base, SessionLocal, engine
from app.models.log import GestureLog
from app.schemas.gesture import InferenceRequest
from app.services.gesture_service import DATASET_SUMMARY, infer_gesture, log_inference

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix='/api', tags=['gestureflow'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/health')
def health():
    return {'status': 'ok'}

@router.post('/infer')
def infer(payload: InferenceRequest, db: Session = Depends(get_db)):
    result = infer_gesture(payload.sample_label, payload.image)
    
    action = result.get('action')
    if action and action != 'none':
        from app.services.action_dispatcher import dispatch_action
        dispatch_action(action)
        
    log_inference(db, result['label'], result['confidence'], result['action'])
    return result

@router.get('/logs/recent')
def logs(db: Session = Depends(get_db)):
    rows = db.query(GestureLog).order_by(GestureLog.id.desc()).limit(20).all()
    return {
        'logs': [
            {
                'id': row.id,
                'predicted_label': row.predicted_label,
                'confidence': row.confidence,
                'action_triggered': row.action_triggered,
                'created_at': row.created_at,
            }
            for row in rows
        ]
    }

@router.get('/dataset/summary')
def dataset_summary():
    from app.services.gesture_service import get_dataset_summary
    return {'summary': get_dataset_summary()}

@router.post('/train/start')
def train_start():
    return {'status': 'queued', 'message': 'Run ml/scripts/train_model.py to train the custom recognizer.'}
