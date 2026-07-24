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

from collections import deque
_gesture_buffer = deque(maxlen=5)
_last_stable_gesture = 'none'

import urllib.request

MODEL_ASSET_PATH = Path(__file__).resolve().parent / "hand_landmarker.task"
if not MODEL_ASSET_PATH.exists():
    print("Downloading hand_landmarker.task...")
    urllib.request.urlretrieve("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task", MODEL_ASSET_PATH)

base_options = mp.tasks.BaseOptions(model_asset_path=str(MODEL_ASSET_PATH))
options = mp.tasks.vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = mp.tasks.vision.HandLandmarker.create_from_options(options)

MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent / 'ml' / 'models' / 'active' / 'gesture_model.joblib'
model = None
if MODEL_PATH.exists():
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print("Failed to load model:", e)

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
    def is_finger_up(tip_idx, pip_idx):
        return landmarks[tip_idx].y < landmarks[pip_idx].y
    
    index_up = is_finger_up(8, 6)
    middle_up = is_finger_up(12, 10)
    ring_up = is_finger_up(16, 14)
    pinky_up = is_finger_up(20, 18)
    
    fingers = [index_up, middle_up, ring_up, pinky_up]
    
    # Robust thumb logic
    index_base_y = landmarks[5].y
    pinky_base_y = landmarks[17].y
    thumb_tip_y = landmarks[4].y
    
    thumb_up = thumb_tip_y < index_base_y - 0.05
    thumb_down = thumb_tip_y > pinky_base_y + 0.05
    
    if fingers == [True, True, True, True]:
        return 'open_palm'
    elif fingers == [False, True, True, True]:
        return 'ok_sign'
    elif fingers == [True, True, False, False]:
        return 'peace'
    elif fingers == [True, False, False, False]:
        return 'index_up'
    elif fingers == [True, False, False, True]:
        return 'metal'
    elif fingers == [False, False, False, True]:
        return 'pinky_up'
    elif fingers == [False, False, False, False]:
        if thumb_up:
            return 'thumbs_up'
        elif thumb_down:
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
                results = detector.detect(mp_image)
                
                if results.hand_landmarks:
                    landmarks = results.hand_landmarks[0]

                    if model is not None:
                        features = []
                        for lm in landmarks:
                            features.extend([lm.x, lm.y, lm.z])
                        pred = model.predict([features])[0]
                        probs = model.predict_proba([features])[0]
                        raw_label = pred
                        confidence = float(max(probs))
                    else:
                        raw_label = heuristic_predict(landmarks)
                        confidence = 0.8
                        
                    _gesture_buffer.append(raw_label)
                    global _last_stable_gesture
                    if len(_gesture_buffer) == 5 and all(x == raw_label for x in _gesture_buffer):
                        _last_stable_gesture = raw_label
                    
                    label = _last_stable_gesture
                else:
                    _gesture_buffer.append('none')
                    if len(_gesture_buffer) == 5 and all(x == 'none' for x in _gesture_buffer):
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
