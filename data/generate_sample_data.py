# data/generate_sample_data.py
# Sample data generator for PhishEye (creates phishing_urls.csv and benign_urls.csv)
import csv
from pathlib import Path

phishing = [
    'http://login-secure-bank.com/verify',
    'http://update-your-account.example.com/login',
    'http://192.168.1.100/secure',
    'http://xn--example-punycode.xn--p1ai/login',
    'http://bit.ly/2fakephish'
]
benign = [
    'https://www.google.com',
    'https://github.com/someuser/somerepo',
    'https://stackoverflow.com/questions',
    'https://www.wikipedia.org',
    'https://www.example.com/about'
]

Path('data').mkdir(parents=True, exist_ok=True)
with open('data/phishing_urls.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for u in phishing:
        writer.writerow([u])

with open('data/benign_urls.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for u in benign:
        writer.writerow([u])

print('Sample datasets created: data/phishing_urls.csv and data/benign_urls.csv')
