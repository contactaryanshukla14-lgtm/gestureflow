import argparse
from pathlib import Path
import cv2

GESTURES = ['open_palm', 'fist', 'thumbs_up', 'peace', 'ok', 'point_left', 'point_right', 'stop', 'none']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True, choices=GESTURES)
    parser.add_argument('--output', default='../data/raw')
    parser.add_argument('--samples', type=int, default=50)
    args = parser.parse_args()

    out_dir = Path(__file__).resolve().parent / args.output / args.label
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(0)
    count = 0
    while count < args.samples:
        ok, frame = cap.read()
        if not ok:
            continue
        preview = frame.copy()
        cv2.putText(preview, f'{args.label} | sample {count+1}/{args.samples}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow('Capture Gesture Dataset', preview)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            cv2.imwrite(str(out_dir / f'{args.label}_{count:04d}.jpg'), frame)
            count += 1
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
