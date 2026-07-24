import json
from pathlib import Path

report = {
    'accuracy': 0.0,
    'precision': 0.0,
    'recall': 0.0,
    'f1_score': 0.0,
    'notes': 'Populate after integrating real training and validation.'
}
path = Path(__file__).resolve().parent.parent / 'models' / 'active' / 'evaluation.json'
path.parent.mkdir(parents=True, exist_ok=True)
with open(path, 'w') as f:
    json.dump(report, f, indent=2)
print('Evaluation stub written to', path)
