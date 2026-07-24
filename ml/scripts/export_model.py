from pathlib import Path
import shutil

src = Path(__file__).resolve().parent.parent / 'models' / 'active' / 'gesture_model.json'
dst = Path(__file__).resolve().parent.parent / 'models' / 'archive' / 'gesture_model_export.json'
dst.parent.mkdir(parents=True, exist_ok=True)
if src.exists():
    shutil.copy2(src, dst)
    print('Exported to', dst)
else:
    print('No active model artifact found.')
