# backend/app.py
# Flask backend for PhishEye (prediction API + SQLite logging)

import os
import sys

# --- FIX: Add project root to Python path ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# -------------------------------------------

from flask import Flask, request, jsonify, g
from flask_cors import CORS
import joblib
import sqlite3
import numpy as np
from model.feature_extractor import extract_basic_features, FEATURE_ORDER

DB_PATH = os.path.join(BASE_DIR, 'backend', 'logger.db')
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'phisheye_rf.joblib')

app = Flask(__name__)
CORS(app)

# load model
pkg = joblib.load(MODEL_PATH)
model = pkg['model']
feature_order = pkg['feature_order']

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    os.makedirs(os.path.join(BASE_DIR, 'backend'), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    score REAL,
                    verdict TEXT,
                    reasons TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'no url provided'}), 400

    # ✅ THIS LINE MUST BE HERE
    feats = extract_basic_features(url)

    vec = np.array([[feats.get(k, 0.0) for k in feature_order]])
    prob = float(model.predict_proba(vec)[0][1])

    threshold = float(data.get('threshold', 0.5))
    pred = 'phishing' if prob >= threshold else 'benign'

    # ---- DEBUG PRINT ----
    print(f"[PREDICT] url={url} prob={prob:.4f} threshold={threshold} pred={pred}")
    # ---------------------


    reasons = []
    if feats.get('has_ip'): reasons.append('IP in URL')
    if feats.get('has_punycode'): reasons.append('Punycode used')
    if feats.get('entropy', 0) > 4.0: reasons.append('High entropy')
    if feats.get('digit_letter_ratio', 0) > 0.3: reasons.append('High numeric ratio')

    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO logs (url, score, verdict, reasons) VALUES (?,?,?,?)',
              (url, prob, pred, ','.join(reasons)))
    conn.commit()

    return jsonify({'url': url, 'score': prob, 'verdict': pred, 'reasons': reasons})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
