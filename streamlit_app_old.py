import streamlit as st
import pickle
import numpy as np
import re
import os
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🔐",
    layout="wide"
)

# ---------------- TITLE ----------------
st.markdown("## 🔐 Phishing URL Detector")
st.write("Enter a URL and check if it is **Phishing** or **Safe**")

# ---------------- LOAD MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model1.pkl")
model = pickle.load(open(MODEL_PATH, "rb"))

# ---------------- FEATURE EXTRACTION ----------------
def extract_features(url):
    return np.array([[
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        1 if "https" in url else 0,
        len(re.findall(r'\d', url))
    ]])

# ---------------- RULE-BASED KEYWORDS ----------------
SUSPICIOUS_KEYWORDS = [
    "free", "gift", "card", "win", "prize",
    "offer", "login", "verify", "secure",
    "update", "reward", "bonus"
]

BRAND_KEYWORDS = [
    "instagram", "facebook", "paypal", "google",
    "microsoft", "apple", "amazon", "netflix",
    "bank", "upi", "whatsapp"
]

def rule_based_phishing(url):
    url_lower = url.lower()
    for word in SUSPICIOUS_KEYWORDS:
        if word in url_lower:
            return True
    for brand in BRAND_KEYWORDS:
        if brand in url_lower and not url_lower.startswith("https://www." + brand):
            return True
    return False

# ---------------- REAL-TIME GOOGLE SAFE BROWSING ----------------
GOOGLE_API_KEY = "PASTE_YOUR_GOOGLE_SAFE_BROWSING_API_KEY_HERE"

def google_safe_browsing_check(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
    payload = {
        "client": {
            "clientId": "phishing-detector",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=5)
        return "matches" in response.json()
    except:
        return False

# ---------------- USER INPUT ----------------
st.markdown("### Enter URL")
url = st.text_input("")

# ---------------- PREDICTION ----------------
if st.button("Check"):
    if url.strip() == "":
        st.warning("Please enter a URL")
    else:
        if google_safe_browsing_check(url):
            st.error("🚨 Phishing")
        elif rule_based_phishing(url):
            st.error("🚨 Phishing")
        elif model.predict(extract_features(url))[0] == 1:
            st.success("✅ Safe")
        else:
            st.error("🚨 Phishing")
