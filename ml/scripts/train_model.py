import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

base = Path(__file__).resolve().parent.parent
processed_csv = base / 'data' / 'processed' / 'features.csv'
model_dir = base / 'models' / 'active'

def train():
    if not processed_csv.exists():
        print(f"Features file not found at {processed_csv}. Run preprocess_dataset.py first.")
        return

    df = pd.DataFrame(pd.read_csv(processed_csv))
    
    train_df = df[df['split'] == 'train']
    test_df = df[df['split'] == 'test']
    
    if len(train_df) == 0:
        print("No training data available. Cannot train.")
        return
        
    X_train = train_df.drop(columns=['label', 'split']).values
    y_train = train_df['label'].values
    
    X_test = test_df.drop(columns=['label', 'split']).values
    y_test = test_df['label'].values
    
    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    if len(X_test) > 0:
        y_pred = clf.predict(X_test)
        print("Evaluation Report:")
        print(classification_report(y_test, y_pred))
    
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, model_dir / 'gesture_model.joblib')
    print('Model exported to', model_dir / 'gesture_model.joblib')

if __name__ == '__main__':
    train()
