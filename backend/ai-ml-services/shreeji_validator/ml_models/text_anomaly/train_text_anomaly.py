# ml_models/text_anomaly/train_text_anomaly.py
import os, pickle
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

DATA_CSV = "data/labels/labels.csv"   # expects columns: text, label (1 real / 0 fake)
OUT_MODEL = "ml_models/text_anomaly/text_anomaly_model.pkl"
TEST_SIZE = 0.2
RANDOM_STATE = 42

def train():
    df = pd.read_csv(DATA_CSV)
    if 'text' not in df.columns or 'label' not in df.columns:
        raise ValueError("labels.csv must contain 'text' and 'label' columns for text anomaly training.")
    X = df['text'].astype(str)
    y = df['label'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
        ("clf", LogisticRegression(max_iter=2000))
    ])

    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    print(classification_report(y_test, preds))

    os.makedirs(os.path.dirname(OUT_MODEL), exist_ok=True)
    with open(OUT_MODEL, "wb") as f:
        pickle.dump(pipe, f)
    print("Saved text anomaly model:", OUT_MODEL)

if __name__ == "__main__":
    train()
