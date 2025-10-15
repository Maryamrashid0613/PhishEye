# model/train.py
"""
Robust training script for PhishEye.

Run from the project root like:
    python -m model.train

This script finds data files relative to the project root (parent of this 'model' folder),
extracts features, trains a RandomForest, prints metrics and saves the model.
"""

from pathlib import Path
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import os
import sys

# Import feature extractor from the model package
# (requires model/__init__.py to exist)
from model.feature_extractor import extract_basic_features, FEATURE_ORDER

# ------------------- Robust path setup -------------------
# BASE_DIR will be the project root (parent of the 'model' folder)
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PHISH = BASE_DIR / 'data' / 'phishing_urls.csv'
DATA_BENIGN = BASE_DIR / 'data' / 'benign_urls.csv'
MODEL_OUT_DIR = BASE_DIR / 'model'
MODEL_OUT = MODEL_OUT_DIR / 'phisheye_rf.joblib'
# ---------------------------------------------------------

os.makedirs(MODEL_OUT_DIR, exist_ok=True)


def load_csv(path: Path) -> pd.DataFrame:
    """
    Load a one-column CSV containing URLs. This function is tolerant of:
      - files with or without header
      - extra whitespace
      - duplicates / empty rows

    Returns a DataFrame with a single column named 'url'.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    # Try reading with header (if file has header row)
    try:
        df = pd.read_csv(path)
    except Exception:
        # fallback to header=None
        df = pd.read_csv(path, header=None, names=['url'])

    # Normalize column name to 'url'
    if 'url' not in df.columns:
        # If first column unnamed, rename
        first_col = df.columns[0]
        df = df.rename(columns={first_col: 'url'})

    # Drop NaN and duplicates and strip whitespace
    df['url'] = df['url'].astype(str).str.strip()
    df = df[df['url'].notna() & (df['url'] != '')]
    # Remove header-like rows if they contain only the word 'url'
    df = df[df['url'].str.lower() != 'url']

    df = df.drop_duplicates().reset_index(drop=True)
    return df


def build_feature_matrix(url_series: pd.Series):
    """
    Given a pandas Series of URLs, return a list-of-lists feature matrix
    following FEATURE_ORDER returned by feature_extractor.
    """
    X = []
    for u in url_series:
        feats = extract_basic_features(u)
        vec = [float(feats.get(k, 0.0)) for k in FEATURE_ORDER]
        X.append(vec)
    return X


def main():
    print(f"Project root detected: {BASE_DIR}")
    print(f"Looking for phishing data at: {DATA_PHISH}")
    print(f"Looking for benign data at:   {DATA_BENIGN}")

    # Load datasets
    phish = load_csv(DATA_PHISH)
    benign = load_csv(DATA_BENIGN)

    phish['label'] = 1
    benign['label'] = 0

    df = pd.concat([phish, benign]).sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"Total examples: {len(df)} (phish: {phish.shape[0]}, benign: {benign.shape[0]})")

    # Build feature matrix
    X = build_feature_matrix(df['url'])
    y = df['label'].values

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # Train a RandomForest baseline
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, digits=4))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save model + feature order for inference
    joblib.dump({'model': clf, 'feature_order': FEATURE_ORDER}, MODEL_OUT)
    print(f"\nSaved model to: {MODEL_OUT}")


if __name__ == '__main__':
    main()
