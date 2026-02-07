import pickle
import numpy as np
import re
import os

# Load Model
try:
    with open("model1.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

def extract_features(url):
    return np.array([[
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        1 if "https" in url else 0,
        len(re.findall(r'\d', url))
    ]])

# Test URLs
test_urls = [
    # Known Safe
    "https://www.google.com",
    "https://www.kerala.gov.in",
    
    # From Training Set (Phishing)
    "http://paypa1-verification.com",
    "http://amaz0n-billing.com",
    
    # New/Unknown variants (Phishing)
    "http://secure-login-paypal.com",
    "http://apple-id-verify.info",
    "http://192.168.1.55/admin"
]

print(f"{'URL':<50} | {'Pred':<5} | {'Conf':<5}")
print("-" * 70)

for url in test_urls:
    features = extract_features(url)
    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0]
    confidence = np.max(prob)
    
    status = "SAFE" if pred == 0 else "PHISH"
    print(f"{url:<50} | {status:<5} | {confidence:.2f}")
