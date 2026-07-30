import base64
import numpy as np
import cv2
import mediapipe as mp
import joblib
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log import GestureLog

ACTION_MAP = {
    'open_palm': 'open_chrome',
    'peace': 'open_whatsapp',
    'index_up': 'open_camera',
    'metal': 'open_calculator',
    'pinky_up': 'open_notepad',
    'ok_sign': 'open_paint',
    'thumbs_up': 'open_folder',
    'thumbs_down': 'open_vscode'
}

from collections import deque, Counter
import math
_gesture_buffer = deque(maxlen=3)
_last_stable_gesture = 'none'

import urllib.request

_detector = None
_model = None
_model_attempted = False

def get_detector():
    global _detector
    if _detector is None:
        try:
            import tempfile
            MODEL_ASSET_PATH = Path(tempfile.gettempdir()) / "hand_landmarker.task"
            if not MODEL_ASSET_PATH.exists():
                print("Downloading hand_landmarker.task...")
                urllib.request.urlretrieve("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task", MODEL_ASSET_PATH)

            base_options = mp.tasks.BaseOptions(model_asset_path=str(MODEL_ASSET_PATH))
            options = mp.tasks.vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
            _detector = mp.tasks.vision.HandLandmarker.create_from_options(options)
        except Exception as e:
            print("Error initializing HandLandmarker:", e)
    return _detector

def get_model():
    global _model, _model_attempted
    if not _model_attempted:
        _model_attempted = True
        MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent / 'ml' / 'models' / 'active' / 'gesture_model.joblib'
        if MODEL_PATH.exists():
            try:
                _model = joblib.load(MODEL_PATH)
            except Exception as e:
                print("Failed to load model:", e)
    return _model

def warmup_models():
    """Asynchronously warm up detector and model after server startup."""
    import threading
    def _warmup():
        print("Warming up ML models in background...")
        get_detector()
        get_model()
        print("ML models warmup complete.")
    threading.Thread(target=_warmup, daemon=True).start()

def get_dataset_summary():
    raw_dir = Path(__file__).resolve().parent.parent.parent.parent / 'ml' / 'data' / 'raw'
    summary = {}
    if raw_dir.exists():
        for d in raw_dir.iterdir():
            if d.is_dir():
                summary[d.name] = len(list(d.glob('*.jpg')))
    if not summary:
        summary = {k: 0 for k in ACTION_MAP.keys()}
        summary['none'] = 0
    return summary

DATASET_SUMMARY = get_dataset_summary() # Initial load, though it would be better as a dynamic property

def heuristic_predict(landmarks):
    # Calculate palm size (wrist to middle finger MCP) for scale invariance
    dx = landmarks[0].x - landmarks[9].x
    dy = landmarks[0].y - landmarks[9].y
    dz = landmarks[0].z - landmarks[9].z
    palm_size = math.sqrt(dx*dx + dy*dy + dz*dz)
    if palm_size < 1e-5:
        return 'none'
        
    def dist(i, j):
        return math.sqrt((landmarks[i].x - landmarks[j].x)**2 + 
                         (landmarks[i].y - landmarks[j].y)**2 + 
                         (landmarks[i].z - landmarks[j].z)**2) / palm_size

    # Check finger extensions (tip further from wrist than PIP & MCP is)
    index_ext = dist(8, 0) > dist(6, 0) and dist(8, 5) > dist(6, 5) * 1.05
    middle_ext = dist(12, 0) > dist(10, 0) and dist(12, 9) > dist(10, 9) * 1.05
    ring_ext = dist(16, 0) > dist(14, 0) and dist(16, 13) > dist(14, 13) * 1.05
    pinky_ext = dist(20, 0) > dist(18, 0) and dist(20, 17) > dist(18, 17) * 1.05
    
    # Check thumb extension (tip further from pinky base or wrist than thumb MCP is)
    thumb_ext = dist(4, 17) > dist(2, 17) * 1.05 and dist(4, 0) > dist(2, 0) * 1.02

    # 1. OK Sign (Thumb and Index tip touching, other 3 extended)
    if dist(4, 8) < 0.5 and middle_ext and ring_ext and pinky_ext:
        return 'ok_sign'
        
    # 2. Open Palm (All 4 fingers extended)
    if index_ext and middle_ext and ring_ext and pinky_ext:
        return 'open_palm'
        
    # 3. Peace Sign (Index & Middle extended, Ring & Pinky curled)
    if index_ext and middle_ext and not ring_ext and not pinky_ext:
        return 'peace'
        
    # 4. Metal (Index & Pinky extended, Middle & Ring curled)
    if index_ext and pinky_ext and not middle_ext and not ring_ext:
        return 'metal'
        
    # 5. Index Up (Only Index extended)
    if index_ext and not middle_ext and not ring_ext and not pinky_ext:
        return 'index_up'
        
    # 6. Pinky Up (Only Pinky extended)
    if pinky_ext and not index_ext and not middle_ext and not ring_ext:
        return 'pinky_up'
        
    # 7. Thumbs Up / Down (4 main fingers curled, thumb extended vertically)
    if not index_ext and not middle_ext and not ring_ext and not pinky_ext:
        # y increases downwards in image coordinates
        if landmarks[4].y < landmarks[5].y - 0.04 and landmarks[4].y < landmarks[0].y - 0.04:
            return 'thumbs_up'
        elif landmarks[4].y > landmarks[5].y + 0.04 and landmarks[4].y > landmarks[0].y + 0.04:
            return 'thumbs_down'

    return 'none'

def infer_gesture(sample_label: str | None, image_b64: str | None = None):
    label = sample_label or 'none'
    confidence = 0.5
    
    if image_b64:
        try:
            if ',' in image_b64:
                image_b64 = image_b64.split(',')[1]
            img_data = base64.b64decode(image_b64)
            np_arr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
                det = get_detector()
                if not det:
                    return {'label': 'none', 'confidence': 0.0, 'action': 'none'}
                results = det.detect(mp_image)
                
                if results.hand_landmarks:
                    landmarks = results.hand_landmarks[0]

                    mod = get_model()
                    if mod is not None:
                        # Normalize landmarks relative to wrist and scale
                        dx = landmarks[0].x - landmarks[9].x
                        dy = landmarks[0].y - landmarks[9].y
                        dz = landmarks[0].z - landmarks[9].z
                        scale = (dx**2 + dy**2 + dz**2)**0.5
                        if scale < 1e-6:
                            scale = 1.0
                            
                        features = []
                        for lm in landmarks:
                            nx = (lm.x - landmarks[0].x) / scale
                            ny = (lm.y - landmarks[0].y) / scale
                            nz = (lm.z - landmarks[0].z) / scale
                            features.extend([nx, ny, nz])
                        
                        pred = mod.predict([features])[0]
                        probs = mod.predict_proba([features])[0]
                        raw_label = pred
                        confidence = float(max(probs))
                    else:
                        raw_label = heuristic_predict(landmarks)
                        confidence = 0.95 if raw_label != 'none' else 0.5
                        
                    _gesture_buffer.append((raw_label, confidence))
                    global _last_stable_gesture
                    
                    # Responsive 3-frame consensus to eliminate single-frame glitch without lag
                    labels = [lbl for lbl, _ in _gesture_buffer]
                    counts = Counter(labels)
                    most_common, count = counts.most_common(1)[0]
                    
                    if most_common != 'none' and count >= 2:
                        _last_stable_gesture = most_common
                    elif most_common == 'none' and count >= 2:
                        _last_stable_gesture = 'none'
                    
                    label = _last_stable_gesture
                    # Boost confidence when stable
                    if label != 'none' and label == raw_label:
                        confidence = max(confidence, 0.98)
                else:
                    _gesture_buffer.append(('none', 0.0))
                    labels = [lbl for lbl, _ in _gesture_buffer]
                    if labels.count('none') >= 2:
                        _last_stable_gesture = 'none'
                    label = _last_stable_gesture
                    confidence = 0.99
        except Exception as e:
            print("Error processing image:", e)
            label = 'none'
            confidence = 0.0

    action = ACTION_MAP.get(label, 'none')
    if label != 'none' and confidence == 0.5:
        confidence = 0.93
    
    return {'label': label, 'confidence': confidence, 'action': action}

def log_inference(db: Session, label: str, confidence: float, action: str):
    row = GestureLog(
        predicted_label=label,
        confidence=confidence,
        action_triggered=action,
        created_at=datetime.utcnow().isoformat()
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
