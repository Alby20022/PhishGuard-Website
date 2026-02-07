import pandas as pd
import re
import numpy as np

# User provided Phishing URLs
phishing_urls = [
    "http://go0gle-login.com", "http://faceboook-security.net", "http://micros0ft-support.com",
    "http://amaz0n-billing.com", "http://paypa1-verification.com", "http://paypal-login-confirm.com",
    "http://facebook-account-check.net", "http://instagram-verify-user.info", "http://google-secure-login.site",
    "http://appleid-reset-password.com", "http://192.168.1.101/login", "http://45.67.89.23/secure",
    "http://103.21.244.0/verify", "http://paypal.com.user-login.verify.ru", "http://google.com.security-update.cn",
    "http://amazon.com.refund.track.ml", "http://facebook.com.recover.account.tk", "http://bit.ly/paypalverify",
    "http://tinyurl.com/google-login", "http://shorturl.at/verify", "http://t.co/accountreset",
    "https://secure-paypal-login.com", "https://facebook-security-check.site", "https://google-support-help.online",
    "https://amazon-refund-center.shop"
]

def extract_features_df(url, label):
    return [
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        1 if "https" in url else 0,
        len(re.findall(r'\d', url)),
        label # Result
    ]

new_data = []
for url in phishing_urls:
    # Clean whitespace
    url = url.strip()
    if url:
        new_data.append(extract_features_df(url, 1)) # Label 1 for Phishing

# Create DataFrame
columns = ["length", "dots", "hyphens", "ats", "https", "digits", "Result"]
new_df = pd.DataFrame(new_data, columns=columns)

# Append to partial csv to avoid messing up if run multiple times, 
# but here we will append to the main one.
# First, let's read existing to check duplicates or just append
try:
    existing_df = pd.read_csv("phishing.csv")
    final_df = pd.concat([existing_df, new_df], ignore_index=True)
    final_df.to_csv("phishing.csv", index=False)
    print(f"Added {len(new_df)} new PHISHING URLs to phishing.csv")
except Exception as e:
    print(f"Error: {e}")
