PhishEye is a machine learning–based phishing detection system that analyzes URLs and predicts whether they are phishing or benign. It provides real-time protection using a Chrome Extension frontend, a Flask backend API, and a Random Forest ML model trained on phishing URL datasets.

Features:
• Real-time phishing URL detection

•	Smart URL feature extraction

•	Machine Learning model (Random Forest)

• Chrome Extension integration

• Fast Flask REST API backend

• User Interface to manually check links

• Instant browser phishing warnings

• URL threat logging using SQLite

• Custom feature extraction module


Dataset & Model Training:

Dataset combined from phishing and benign URL datasets (Kaggle). Custom feature extraction (URL length, HTTPS check, entropy, digit ratio, special characters). Model: Random Forest Classifier saved as phisheye_rf.joblib.

Tech Stack:

Component	Technology

Frontend	Chrome Extension

Backend 	Flask API (Python)

ML Model	Scikit-learn (Random Forest)

Database	SQLite

Packaging	Joblib


Project Structure:

PhishEye/

├── backend/ → Flask app + logger database

├── model/ → Training script + ML model + feature extractor

├── extension/ → Chrome extension files

└── README.md


Setup Instructions:

1. Clone Repository:

   git clone https://github.com/maryamrashid0613/PhishEye.git
   
2. Install & run backend:
   
   cd backend
   pip install -r requirements.txt
   python app.py
   
3. Load Chrome extension:
   
   Open Chrome → Extensions → Enable Developer Mode → Load unpacked → select extension folder
   

Security Features:

 Real-time phishing alerts
 
 Browser blocking + warning
 
 URL risk scoring
 
 Logs suspicious activity
 
