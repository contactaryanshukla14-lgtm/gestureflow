import pandas as pd
from pathlib import Path
import random
import shutil
import cv2
import mediapipe as mp
import numpy as np

RAW = Path(__file__).resolve().parent.parent / 'data' / 'raw'
SPLITS = Path(__file__).resolve().parent.parent / 'data' / 'splits'
PROCESSED = Path(__file__).resolve().parent.parent / 'data' / 'processed'
RATIOS = {'train': 0.7, 'val': 0.15, 'test': 0.15}

import urllib.request

MODEL_ASSET_PATH = Path(__file__).resolve().parent.parent / "models" / "hand_landmarker.task"
if not MODEL_ASSET_PATH.exists():
    MODEL_ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task", MODEL_ASSET_PATH)

base_options = mp.tasks.BaseOptions(model_asset_path=str(MODEL_ASSET_PATH))
options = mp.tasks.vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = mp.tasks.vision.HandLandmarker.create_from_options(options)

def extract_features(img_path):
    img = cv2.imread(str(img_path))
    if img is None:
        return None
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    results = detector.detect(mp_image)
    
    if not results.hand_landmarks:
        return None
    
    landmarks = results.hand_landmarks[0]
    
    # Calculate normalization scale (distance from wrist to middle finger MCP)
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
    return features

def split_and_extract():
    for split in RATIOS:
        (SPLITS / split).mkdir(parents=True, exist_ok=True)
    
    PROCESSED.mkdir(parents=True, exist_ok=True)
    dataset = []

    for label_dir in [p for p in RAW.iterdir() if p.is_dir()]:
        files = [p for p in label_dir.iterdir() if p.is_file()]
        random.shuffle(files)
        n = len(files)
        a = int(n * RATIOS['train'])
        b = a + int(n * RATIOS['val'])
        buckets = {'train': files[:a], 'val': files[a:b], 'test': files[b:]}
        
        for split, items in buckets.items():
            target = SPLITS / split / label_dir.name
            target.mkdir(parents=True, exist_ok=True)
            for file in items:
                shutil.copy2(file, target / file.name)
                
                # Extract features for dataset
                feat = extract_features(file)
                if feat is not None:
                    dataset.append([label_dir.name, split] + feat)
                    
    if dataset:
        cols = ['label', 'split'] + [f'feat_{i}' for i in range(len(dataset[0]) - 2)]
        df = pd.DataFrame(dataset, columns=cols)
        df.to_csv(PROCESSED / 'features.csv', index=False)
        print(f"Extracted {len(dataset)} valid frames to features.csv")
    else:
        print("No valid hands found in dataset. Make sure you captured some data.")
        
    print('Dataset split and feature extraction complete.')

if __name__ == '__main__':
    split_and_extract()
