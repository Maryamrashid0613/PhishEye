# model/feature_extractor.py
# Feature extractor for PhishEye

import re
import numpy as np
import tldextract

SUSPICIOUS_TOKENS = ['login', 'secure', 'update', 'account', 'verify', 'confirm', 'signin', 'bank', 'paypal']

ip_regex = re.compile(r"https?://(\d{1,3}(?:\.\d{1,3}){3})(?:[:/]|$)")

def entropy(s: str) -> float:
    if not s:
        return 0.0
    probs = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * np.log2(p) for p in probs if p > 0)

def extract_basic_features(url: str) -> dict:
    url = str(url).strip()
    features = {}
    features['url_len'] = len(url)
    features['num_dots'] = url.count('.')
    features['num_slash'] = url.count('/')
    features['num_hyphen'] = url.count('-')
    features['num_at'] = url.count('@')
    features['num_qm'] = url.count('?')
    features['num_eq'] = url.count('=')
    features['num_pct'] = url.count('%')
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_upper'] = sum(1 for c in url if c.isupper())
    features['has_https'] = 1 if url.lower().startswith('https') else 0
    features['has_ip'] = 1 if ip_regex.search(url) else 0
    features['has_punycode'] = 1 if 'xn--' in url.lower() else 0
    features['entropy'] = entropy(url)

    try:
        ext = tldextract.extract(url)
        hostname = '.'.join(part for part in [ext.subdomain, ext.domain, ext.suffix] if part)
    except Exception:
        hostname = ''
    features['host_len'] = len(hostname)
    features['subdomain_count'] = hostname.count('.') if hostname else 0

    low = url.lower()
    for tok in SUSPICIOUS_TOKENS:
        features[f'tok_{tok}'] = 1 if tok in low else 0

    letters = sum(c.isalpha() for c in url)
    features['digit_letter_ratio'] = features['num_digits'] / (letters + 1e-6)
    return features

FEATURE_ORDER = [
    'url_len','num_dots','num_slash','num_hyphen','num_at','num_qm','num_eq','num_pct',
    'num_digits','num_upper','has_https','has_ip','has_punycode','entropy','host_len',
    'subdomain_count'
] + [f'tok_{tok}' for tok in SUSPICIOUS_TOKENS] + ['digit_letter_ratio']
