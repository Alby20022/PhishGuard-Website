
import streamlit as st
import pickle
import numpy as np
import re
import os
import requests
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="PhishGuard - Advanced URL Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* GLOBAL THEME */
    body {
        background-color: #0A0B1A;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    
    /* FORCE SINGLE PAGE LAYOUT */
    .stApp {
        background: #0A0B1A;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 210, 255, 0.1) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(0, 255, 157, 0.1) 0%, transparent 20%);
        height: 100vh;
        overflow: hidden; /* Remove scrolling */
    }
    
    /* CONTENT CONTAINER ALIGNMENT */
    .block-container {
        padding-top: 2rem !important; /* Top align menu */
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100%;
    }
    
    /* REMOVE DEFAULT STREAMLIT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* NAVBAR */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(10, 11, 26, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        height: 70px;
    }
    .logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d2ff;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .nav-links {
        display: flex;
        gap: 2rem;
    }
    .nav-item {
        color: #a0a0b0;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
        transition: color 0.3s;
        background: none;
        border: none;
        padding: 0;
        font-size: 1rem;
    }
    .nav-item:hover, .nav-item.active {
        color: #ffffff;
    }
    .logout-btn {
        background: rgba(255, 59, 48, 0.15);
        color: #ff3b30;
        border: 1px solid rgba(255, 59, 48, 0.3);
        padding: 0.4rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .logout-btn:hover {
        background: rgba(255, 59, 48, 0.3);
        transform: translateY(-1px);
    }
    
    /* HERO SECTION */
    .hero {
        text-align: center;
        padding: 8rem 2rem 4rem;
    }
    .hero h1 {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d2ff 0%, #00ff9d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }
    .hero p {
        font-size: 1.25rem;
        color: #a0a0b0;
        max-width: 600px;
        margin: 0 auto 3rem;
        line-height: 1.6;
    }
    
    /* CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* INPUTS */
    div[data-baseweb="input"] {
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    /* BUTTON STYLING */
    /* Primary (CTA) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #00d2ff, #00aaff) !important;
        color: #000 !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.5) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.8) !important;
        color: #fff !important;
    }

    /* Secondary (Navbar Links) - Redesigned with !important to force overrides */
    div.stButton > button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid transparent !important; 
        color: #B0B0C0 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important; /* Larger visibility */
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    /* Hover Effect: Explicit Background Highlight */
    div.stButton > button[kind="secondary"]:hover {
        color: #00ff9d !important;
        border: 1px solid rgba(0, 255, 157, 0.3) !important;
        background-color: rgba(0, 255, 157, 0.1) !important; /* Visible Highlight */
        text-shadow: 0 0 8px rgba(0, 255, 157, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Focus State */
    div.stButton > button[kind="secondary"]:focus:not(:active) {
        border-color: #00d2ff !important;
        color: #00d2ff !important;
    }/* DATAFRAME */
    div[data-testid="stDataFrame"] {
        background: rgba(0,0,0,0.2);
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# ---------------- NAVIGATION ----------------
def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

def logout():
    st.session_state['auth'] = False
    st.session_state['page'] = 'home'
    st.rerun()

def render_navbar():
    # Navbar CSS is now handled globally via specific types
    
    if st.session_state['auth']:
        # Layout: Logo (Left) | Spacer | Nav Items (Right)
        # Increased right column width to prevent text wrapping
        col1, col2, col3 = st.columns([2, 4, 7])
        
        with col1:
             st.markdown('<div class="logo">🛡️ PhishGuard</div>', unsafe_allow_html=True)
        
        with col3:
            # Menu Items - closer together
            n1, n2, n3, n4, n5 = st.columns([1, 1, 1.5, 1, 1], gap="small")
            
            with n1: 
                # Secondary (Default) buttons will now look like text links due to CSS above
                if st.button("Upload", key="nav_up", type="secondary", use_container_width=True): navigate_to('dashboard')
            with n2: 
                if st.button("Scanner", key="nav_scan", type="secondary", use_container_width=True): navigate_to('scanner')
            with n3: 
                if st.button("Performance", key="nav_perf", type="secondary", use_container_width=True): navigate_to('performance')
            with n4: 
                if st.button("Graphs", key="nav_charts", type="secondary", use_container_width=True): navigate_to('charts')
            with n5: 
                if st.button("Logout", key="nav_logout", type="secondary", use_container_width=True): logout()
        
    else:
        # Home/Login Page Navbar - Logo aligns Left now
        col1, col2 = st.columns([2, 8])
        with col1:
            st.markdown('<div class="logo">🛡️ PhishGuard</div>', unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True) # Minimal Spacer, No Border

# ---------------- LOGIC ----------------
# Load Model
@st.cache_resource
def load_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "model1.pkl")
    try:
        model = pickle.load(open(MODEL_PATH, "rb"))
        return model
    except Exception as e:
        return None

model = load_model()

def extract_features(url):
    return np.array([[
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        1 if "https" in url else 0,
        len(re.findall(r'\d', url))
    ]])

def analyze_risk_factors(url, features):
    risks = []
    # Heuristic Checks
    if len(url) > 75: risks.append("Suspiciously long URL")
    if url.count('.') > 3: risks.append("High dot count (Obfuscation)")
    if url.count('-') > 3: risks.append("High hyphen usage")
    if url.count('@') > 0: risks.append("URL concealment (@ detected)")
    if features[0][5] > 5: risks.append("High numeric character count")
    
    # Check TLD
    valid_tlds = ['.com', '.org', '.net', '.edu', '.gov', '.io', '.co', '.ai', '.in', '.us', '.uk']
    if not any(tld in url.lower() for tld in valid_tlds):
        risks.append("Uncommon TLD")
        
    if not risks and features[0][4] == 0:
        risks.append("Not using valid HTTPS")
        
    return risks

def predict_url_sophisticated(url):
    # 1. Extended Whitelist
    safe_domains = [
        "google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org", 
        "instagram.com", "twitter.com", "linkedin.com", "netflix.com", "microsoft.com", 
        "apple.com", "github.com", "stackoverflow.com", "openai.com", "reddit.com",
        "snapchat.com", "tiktok.com", "paypal.com", "visa.com", "mastercard.com",
        "hdfcbank.com", "sbi.co.in", "icicibank.com", "india.gov.in", "uidai.gov.in",
        "kerala.gov.in", "nptel.ac.in", "coursera.org", "edx.org"
    ]
    
    for domain in safe_domains:
        if domain in url.lower(): 
            return {
                "class": 0, 
                "confidence": 1.0, 
                "risks": [], 
                "reason": "Whitelisted Trusted Domain"
            }

    # 2. Extract Features
    try:
        features = extract_features(url)
    except:
        return {"class": 1, "confidence": 0.0, "risks": ["Error parsing URL"], "reason": "Error"}

    # 3. Model Prediction
    if model:
        try:
            # Get probability if available
            prediction = model.predict(features)[0]
            confidence = np.max(model.predict_proba(features)) if hasattr(model, 'predict_proba') else 0.95
            
            risks = analyze_risk_factors(url, features)
            
            # Hybrid override: If model says Safe but has many risks, lower confidence or flag
            if prediction == 0 and len(risks) >= 2:
                confidence = max(0.6, confidence - 0.2) # Reduce confidence
            
            return {
                "class": prediction,
                "confidence": float(confidence),
                "risks": risks,
                "reason": "Model Prediction"
            }
        except Exception as e:
            return {"class": 1, "confidence": 0.0, "risks": [f"Model Error: {str(e)}"], "reason": "Error"}
            
    # 4. Fallback
    return {"class": 1, "confidence": 0.5, "risks": ["Model not loaded"], "reason": "Fallback"}

# ---------------- PAGES ----------------

def render_home():
    # Navbar only has Logo and Login
    render_navbar()
    
    # CSS Removed - Handled Globally now
    
    # Content Container - using margin-top to position "just below" as requested previously
    
    # Content Container - using margin-top to position "just below" as requested previously
    
    st.markdown("""
    <div style="
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        text-align: center; 
        margin-top: 15vh; /* Reverted to spacing */
        margin-bottom: 2rem;
    ">
        <h1 style="
            font-size: 3.5rem; 
            background: linear-gradient(135deg, #00d2ff 0%, #00ff9d 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        ">Malicious and Phishing URL Detection<br>Using Machine Learning</h1>
        <p style="
            color: #a0a0b0; 
            font-size: 1.1rem; 
            margin-top: 1rem;
            max-width: 700px;
        ">
            Advanced AI-powered URL detection system that identifies Phishing and malicious websites before they can harm you
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Button Centered
    col1, col2, col3 = st.columns([1, 0.4, 1])
    with col2:
        if st.button("Start Scanning URLs 🚀", type="primary"):
            navigate_to('login')

def render_login():
    render_navbar()
    
    # Login Page Specific CSS
    st.markdown("""
        <style>
               /* Page Layout */
               .stApp { height: 100vh; overflow: hidden; }
               .block-container {
                    display: flex;
                    flex-direction: column; 
                    justify-content: center;
                    align-items: center;
                }
               [data-testid="stHeader"] { display: none; }
               
               /* Login Card Glow Effect */
               .login-card {
                   background: #0A0B1A;
                   border: 1px solid #00d2ff;
                   border-radius: 20px;
                   padding: 3rem;
                   box-shadow: 0 0 30px rgba(0, 210, 255, 0.2);
                   text-align: center;
                   max-width: 450px;
                   margin: 0 auto;
               }
               
               /* Input Fields Styling */
               div[data-baseweb="input"] {
                   background-color: #0f1125 !important;
                   border: 1px solid #00d2ff !important;
                   border-radius: 8px !important;
                   color: white !important;
                   position: relative; /* For icon positioning */
               }
               div[data-baseweb="input"] input {
                   color: white !important;
                   padding-left: 3rem !important; /* Space for icon */
               }
               
               /* Icons inside Input Fields */
               
               /* Username Icon - Targets Input with label "Username" */
               div[data-testid="stTextInput"] div[data-baseweb="input"]:has(input[aria-label="Username"])::before {
                   content: "👤"; /* User Icon */
                   position: absolute;
                   left: 10px;
                   top: 50%;
                   transform: translateY(-50%);
                   font-size: 1.2rem;
                   z-index: 5;
               }
               
               /* Password Icon - Targets Input with label "Password" */
               div[data-testid="stTextInput"] div[data-baseweb="input"]:has(input[aria-label="Password"])::before {
                   content: "🔒"; /* Lock Icon */
                   position: absolute;
                   left: 10px;
                   top: 50%;
                   transform: translateY(-50%);
                   font-size: 1.2rem;
                   z-index: 5;
               }

               /* Labels */
               .stTextInput label {
                   color: #00d2ff !important;
                   font-weight: 600;
               }
        </style>
    """, unsafe_allow_html=True)
    
    # Use columns to center the fixed-width card
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-card">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔐</div>
            <h1 style="color: #00d2ff; font-weight: 800; margin-bottom: 0.5rem; font-size: 2.5rem;">Login</h1>
            <p style="color: #888; font-size: 0.9rem; margin-bottom: 2rem;">Malicious and Phishing URL Detection Using<br>Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Inputs placed INSIDE the visual card flow (by optical alignment via columns or just below in the same container flow)
        # To truly put them "inside" the HTML card we would need to write raw HTML forms which breaks Streamlit state.
        # Instead, we visually mimic it by continuing the div context or relying on the background color match.
        # However, since we can't inject Streamlit widgets into an open HTML div, we will stick to the visual grouping.
        # Actually, let's just use the transparent background for widgets and rely on the container.
        
        # NOTE: Streamlit widgets cannot be nested in st.markdown HTML. 
        # So we use a visual container approach: 
        # The CSS above sets a background on the inputs.
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Login to Dashboard", type="primary", use_container_width=True):
            if username == "admin" and password == "admin":
                st.session_state['auth'] = True
                st.success("Login successful!")
                time.sleep(1)
                navigate_to('dashboard')
            else:
                st.error("Invalid Username or Password")
        
        st.markdown("""
            <div style="text-align: center; margin-top: 1.5rem;">
                <p style="color: #00d2ff; cursor: pointer; opacity: 0.8;">← Back to Home</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Back Button logic (invisible button over text or just a button)
        # Using a button for functionality
        if st.button("Back to Home", key="back_home_btn", type="secondary", use_container_width=True):
             navigate_to('home')

def render_dashboard():
    render_navbar()
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 0.5rem; color: #00d2ff;'>Upload Dataset</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; margin-bottom: 2rem;'>Upload your phishing dataset for analysis</p>", unsafe_allow_html=True)
    
    # Center Column for the Card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Anchor for CSS targeting
        st.markdown('<span id="dashboard-card-anchor"></span>', unsafe_allow_html=True)
        
        # Custom CSS for Dashboard Uploader & Card
        st.markdown("""
            <style>
                /* Glass Card Container */
                div[data-testid="stVerticalBlock"]:has(span#dashboard-card-anchor) {
                    background: rgba(15, 17, 37, 0.7);
                    border: 1px solid rgba(0, 210, 255, 0.1);
                    border-radius: 20px;
                    padding: 3rem;
                    box-shadow: 0 0 30px rgba(0,0,0,0.5);
                    text-align: center;
                }
                
                /* Native File Uploader Styling */
                section[data-testid="stFileUploaderDropzone"] {
                    border: 2px dashed #00d2ff !important;
                    background-color: rgba(0, 210, 255, 0.05) !important;
                    border-radius: 10px !important;
                    padding: 3rem 2rem !important; /* More vertical padding */
                    transition: all 0.3s ease;
                    min-height: 150px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                }
                section[data-testid="stFileUploaderDropzone"]:hover {
                     background-color: rgba(0, 210, 255, 0.1) !important;
                     border-color: #00ff9d !important;
                     cursor: pointer;
                }
                
                /* Hide Default Content overlay for custom look - aggressive hiding */
                section[data-testid="stFileUploaderDropzone"] div,
                section[data-testid="stFileUploaderDropzone"] button,
                section[data-testid="stFileUploaderDropzone"] span,
                section[data-testid="stFileUploaderDropzone"] small,
                section[data-testid="stFileUploaderDropzone"] svg {
                    opacity: 0 !important;
                }
                
                /* Custom Content via Pseudo-element */
                section[data-testid="stFileUploaderDropzone"]::before {
                    content: "📂 Click to browse or drag & drop your file here\\000ASupported formats: CSV, XLSX (Max 200MB)";
                    white-space: pre-wrap; /* Allow newlines */
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: #B0B0C0;
                    font-size: 1.1rem;
                    text-align: center;
                    z-index: 1;
                    pointer-events: none;
                    line-height: 1.6;
                }
            </style>
        """, unsafe_allow_html=True)

    with col2:
        # Header Content
        st.markdown("""
            <div style="font-size: 4rem; margin-bottom: 1rem; display: flex; justify-content: center;">
                📊
            </div>
            <h3 style="color: #00d2ff; margin-bottom: 1.5rem; font-weight: 600; text-align: center;">Select Dataset File</h3>
        """, unsafe_allow_html=True)
        
        # Real Uploader - Now it IS the dashed box
        uploaded_file = st.file_uploader("Browse File", type=['csv', 'xlsx'], key="dash_uploader", label_visibility="collapsed")
        
        # Explicit confirmation button logic - ALWAYS VISIBLE now
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Custom button styling wrapper to match the dark look if needed, 
        # but using type="primary" with our global CSS is the closest start.
        # We might need to override the specific button color to be dark if the image suggests it,
        # but for now let's stick to the theme's primary button but with the right text/icon.
        
        if st.button("☁️ Upload Dataset", type="primary", use_container_width=True):
             if uploaded_file is not None:
                 try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state['uploaded_df'] = df
                    st.session_state['uploaded_filename'] = uploaded_file.name
                    st.success("File Uploaded Successfully! Redirecting...")
                    time.sleep(1)
                    navigate_to('dataset_overview')
                 except Exception as e:
                     st.error(f"Error reading file: {e}")
             else:
                 st.warning("Please select a file first.")

# ---------------- DATASET OVERVIEW PAGE ----------------
def render_dataset_overview():
    render_navbar()
    
    if 'uploaded_df' not in st.session_state:
        st.warning("No data found. Please upload a dataset first.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Go to Upload", type="primary"):
            navigate_to('dashboard')
        return

    df = st.session_state['uploaded_df']
    filename = st.session_state.get('uploaded_filename', 'dataset.csv')
    
    st.markdown(f"<h2 style='text-align: center; color: #00d2ff; margin-bottom: 0px;'>Dataset Overview</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888; margin-bottom: 2rem;'>Viewing: {filename}</p>", unsafe_allow_html=True)
    
    # Custom CSS for Logic Cards
    st.markdown("""
        <style>
            .stat-card {
                background: rgba(15, 17, 37, 0.7);
                border: 1px solid rgba(0, 210, 255, 0.2);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                transition: transform 0.3s ease;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .stat-card:hover {
                transform: translateY(-5px);
                border-color: #00ff9d;
                box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
            }
            .stat-icon {
                font-size: 2.5rem;
                margin-bottom: 1rem;
            }
            .stat-label {
                color: #00d2ff;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            .stat-value {
                color: #fff;
                font-size: 1.5rem;
                font-weight: 700;
            }
        </style>
    """, unsafe_allow_html=True)

    # 3 Column Layout for Stats
    c1, c2, c3 = st.columns(3, gap="medium")
    
    with c1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-label">Total Rows</div>
                <div class="stat-value">{df.shape[0]}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-label">Total Columns</div>
                <div class="stat-value">{df.shape[1]}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-icon">📁</div>
                <div class="stat-label">File Format</div>
                <div class="stat-value">CSV</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Start Scanner Button Centered
    bc1, bc2, bc3 = st.columns([1, 1, 1])
    with bc2:
        if st.button("🔍 Start URL Scanner", type="primary", use_container_width=True):
            navigate_to('scanner')
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dataset Preview styled
    st.markdown("""
        <div style="background: rgba(15, 17, 37, 0.7); padding: 10px; border-radius: 10px; border: 1px solid rgba(0,210,255,0.1);">
            <h3 style="color: #00d2ff; margin-left:10px;">📊 Dataset Preview</h3>
        </div>
        <br>
    """, unsafe_allow_html=True)
    
    st.dataframe(df.head(100), use_container_width=True)

def render_scanner():
    render_navbar()
    
    # Custom CSS for Scanner Page - Split Layout
    st.markdown("""
        <style>
            /* Header Center */
            .scanner-title {
                text-align: center;
                font-size: 3rem;
                font-weight: 700;
                color: #00d2ff;
                margin-bottom: 3rem;
                text-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
            }
            
            /* Left Column: Input Card Styling */
            /* Target the specific container using the anchor */
            div[data-testid="stVerticalBlock"]:has(span#scanner-input-anchor) {
                background: #0A0B1A;
                border: 1px solid rgba(0, 210, 255, 0.2);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 0 40px rgba(0,0,0,0.5);
                height: 100%;
            }

            .scanner-label {
                color: #00d2ff;
                font-weight: 600;
                margin-bottom: 0.5rem;
                font-size: 1rem;
                text-align: left;
            }
            
            /* Custom Input Styling */
            .stTextInput input {
                background-color: #0f1125 !important;
                border: 1px solid #334466 !important;
                color: #fff !important;
                border-radius: 8px !important;
                padding: 10px 15px !important;
            }
            .stSelectbox div[data-baseweb="select"] div {
                 background-color: #0f1125 !important;
                 color: #fff !important;
                 border-color: #334466 !important;
            }
            
            /* Right Column: Result Section */
            .result-container {
                height: 100%;
                min-height: 400px; /* Match height of input card roughly */
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 2rem;
                border: 1px solid #334466;
                border-radius: 20px;
                background: rgba(15, 17, 37, 0.6);
                text-align: center;
                animation: fadeIn 0.5s ease-in;
            }
            .safe-icon {
                font-size: 5rem;
                color: #00ff9d;
                margin-bottom: 1rem;
            }
            .url-display {
                background: #0A0B1A;
                padding: 15px;
                border-radius: 8px;
                color: #aaa;
                width: 100%;
                margin: 2rem 0;
                border: 1px solid #334466;
                font-family: monospace;
                word-break: break-all;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="scanner-title">🔍 URL Scanner</div>', unsafe_allow_html=True)
    
    # Split Layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        # Invisible Anchor for CSS targeting of the Input Card
        st.markdown('<span id="scanner-input-anchor"></span>', unsafe_allow_html=True)
        
        st.markdown('<div class="scanner-label">Select ML Model</div>', unsafe_allow_html=True)
        model_map = {
            "🌳 Gradient Boosting Classifier": "Gradient Boosting Classifier",
            "⚡ XGBoost Classifier": "XGBoost Classifier",
            "🌲 Random Forest": "Random Forest",
            "🔧 Support Vector Machine": "Support Vector Machine"
        }
        selected_option = st.selectbox("", list(model_map.keys()), label_visibility="collapsed")
        model_choice = model_map[selected_option]
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        st.markdown('<div class="scanner-label">Enter URL to Scan</div>', unsafe_allow_html=True)
        url_input = st.text_input("", placeholder="https://example.com...", label_visibility="collapsed")
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        scan_pressed = st.button("Analyze URL", type="primary", use_container_width=True)
        
    with col_right:
        # Initialize Scan History if not present
        if 'scan_history' not in st.session_state:
            st.session_state['scan_history'] = []

        if scan_pressed and url_input:
            # 1. Prediction
            pred_data = predict_url_sophisticated(url_input)
            result = pred_data["class"]
            confidence = pred_data["confidence"]
            risks = pred_data["risks"]
            
            target_url = url_input if url_input.startswith(('http://', 'https://')) else f'https://{url_input}'
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # 2. Log Activity
            status_text = "SAFE" if result == 0 else "PHISHING"
            st.session_state['scan_history'].insert(0, {
                "Time": timestamp, 
                "URL": url_input, 
                "Status": status_text,
                "Action": "Allowed" if result == 0 else "Blocked"
            })
            
            # 3. Display Result logic
            # Define Thresholds
            CONFIDENCE_THRESHOLD = 0.80
            
            # Logic Branching
            is_high_confidence = confidence >= CONFIDENCE_THRESHOLD
            
            if result == 0 and is_high_confidence: # DEFINITELY SAFE
                st.markdown(f"""<div class="result-container" style="border-color: #00ff9d; background: linear-gradient(180deg, rgba(0,255,157,0.1) 0%, rgba(0,0,0,0) 100%);">
<div class="safe-icon">✅</div>
<h2 style="color: #00ff9d; margin-bottom: 0.5rem; text-shadow: 0 0 10px rgba(0,255,157,0.5);">SAFE WEBSITE</h2>
<h3 style="color: #fff; margin-bottom: 0.5rem;">ACCESS GRANTED</h3>
<div style="margin-bottom: 1rem; color: #00ff9d; font-weight: bold;">Confirmation: {pred_data['reason']} ({int(confidence*100)}%)</div>
<div class="url-display">{target_url}</div>
<a href="{target_url}" target="_blank" style="text-decoration: none;">
<button style="background: #00ff9d; color: #000; border: none; padding: 12px 30px; border-radius: 5px; font-weight: bold; cursor: pointer; font-size: 1.1rem; box-shadow: 0 0 15px rgba(0,255,157,0.4);">
🚀 PROCEED TO SITE
</button>
</a>
</div>""", unsafe_allow_html=True)
                
                # Show Risks if any (informational)
                if risks:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("ℹ️  Site Notices", expanded=False):
                        for risk in risks:
                            st.write(f"- {risk}")

            elif result == 1 and is_high_confidence: # DEFINITELY PHISHING
                st.markdown(f"""<div class="result-container" style="border-color: #ff3333; background: linear-gradient(180deg, rgba(255,51,51,0.15) 0%, rgba(0,0,0,0) 100%);">
<div class="safe-icon" style="color: #ff3333;">🚫</div>
<h2 style="color: #ff3333; margin-bottom: 0.5rem; text-shadow: 0 0 15px rgba(255,51,51,0.6);">PHISHING DETECTED</h2>
<h3 style="color: #fff; margin-bottom: 0.5rem;">ACCESS DENIED</h3>
<div style="margin-bottom: 1rem; color: #ff3333; font-weight: bold;">Confirmation: {pred_data['reason']} ({int(confidence*100)}%)</div>
<p style="color: #ffaaaa; margin-bottom: 2rem;">This site has been permanently blocked for your safety.</p>
<div class="url-display" style="border-color: #ff3333; color: #ff3333;">{target_url}</div>
<button style="background: #333; color: #aaa; border: 1px solid #555; padding: 10px 20px; border-radius: 5px; cursor: not-allowed;">
🔒 BLOCKED
</button>
</div>""", unsafe_allow_html=True)
                
                # Detailed Risks
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="scanner-label">🧐 Risk Analysis Report</div>', unsafe_allow_html=True)
                for risk in risks:
                    st.markdown(f"""<div style="background: rgba(255, 51, 51, 0.1); border-left: 3px solid #ff3333; padding: 10px; margin-bottom: 5px; border-radius: 0 5px 5px 0;">
<span style="color: #ffaaaa;">⚠️ {risk}</span>
</div>""", unsafe_allow_html=True)

            else: # CAUTION / UNCERTAIN (Low Confidence)
                st.markdown(f"""<div class="result-container" style="border-color: #ffcc00; background: linear-gradient(180deg, rgba(255,204,0,0.1) 0%, rgba(0,0,0,0) 100%);">
<div class="safe-icon" style="color: #ffcc00;">⚠️</div>
<h2 style="color: #ffcc00; margin-bottom: 0.5rem; text-shadow: 0 0 15px rgba(255,204,0,0.5);">POTENTIAL RISK</h2>
<h3 style="color: #fff; margin-bottom: 0.5rem;">CAUTION ADVISED</h3>
<div style="margin-bottom: 1rem; color: #ffcc00; font-weight: bold;">Uncertainty Level: {int((1-confidence)*100)}% (Confidence: {int(confidence*100)}%)</div>
<p style="color: #ffeeb0; margin-bottom: 1rem;">The model detected some suspicious patterns but is not 100% sure.</p>
<div class="url-display" style="border-color: #ffcc00; color: #ffcc00;">{target_url}</div>

<div style="display: flex; gap: 10px; justify-content: center; width: 100%;">
<a href="{target_url}" target="_blank" style="text-decoration: none; flex: 1;">
<button style="background: transparent; border: 2px solid #ffcc00; color: #ffcc00; padding: 12px 10px; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; transition: all 0.3s;">
⚠️ PROCEED (UNSAFE)
</button>
</a>
<button style="background: #ffcc00; color: #000; border: none; padding: 12px 10px; border-radius: 5px; font-weight: bold; cursor: not-allowed; flex: 1; opacity: 0.7;">
🔍 SCAN AGAIN
</button>
</div>
</div>""", unsafe_allow_html=True)
                
                # Show Risks that caused the caution
                if risks:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="scanner-label">⚠️ Risk Factors Found</div>', unsafe_allow_html=True)
                    for risk in risks:
                        st.markdown(f"""<div style="background: rgba(255, 204, 0, 0.1); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 5px; border-radius: 0 5px 5px 0;">
<span style="color: #ffeeb0;">🔸 {risk}</span>
</div>""", unsafe_allow_html=True)
        
        # 4. Live Tracking Log (Show always if history exists)
        if 'scan_history' in st.session_state and st.session_state['scan_history']:
            st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)
            st.markdown('<div class="scanner-label">📡 Real-time Tracking Activity</div>', unsafe_allow_html=True)
            
            # Create DataFrame for display
            history_df = pd.DataFrame(st.session_state['scan_history'])
            
            # Styling the dataframe
            st.dataframe(
                history_df,
                use_container_width=True,
                column_config={
                    "Time": st.column_config.TextColumn("Time", width="small"),
                    "URL": st.column_config.TextColumn("URL", width="large"),
                    "Status": st.column_config.TextColumn("Status", width="medium"),
                    "Action": st.column_config.TextColumn("Action", width="medium"),
                },
                hide_index=True
            )
        else:
            # Placeholder State for Right Column
             st.markdown("""<div class="result-container" style="justify-content: center; opacity: 0.5;">
<div style="font-size: 6rem; color: #334466; margin-bottom: 2rem;">🛡️</div>
<h3 style="color: #556688;">Ready to Scan</h3>
<p style="color: #445566;">Enter a URL on the left to begin analysis</p>
</div>""", unsafe_allow_html=True)

def render_performance():
    render_navbar()
    
    # Custom CSS for Performance Page
    st.markdown("""
        <style>
            .perf-header {
                text-align: center;
                font-size: 2.5rem;
                font-weight: 700;
                color: #fff;
                margin-bottom: 2rem;
                text-shadow: 0 0 20px rgba(0, 210, 255, 0.5);
            }
            .glass-panel {
                background: rgba(15, 17, 37, 0.7);
                border: 1px solid rgba(0, 210, 255, 0.2);
                border-radius: 15px;
                padding: 1.5rem;
                box-shadow: 0 0 20px rgba(0,0,0,0.3);
                margin-bottom: 2rem;
            }
            
            /* Custom Table Styles */
            .styled-table {
                width: 100%;
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.9em;
                font-family: sans-serif;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                border-radius: 10px;
                overflow: hidden;
            }
            .styled-table thead tr {
                background-color: #00d2ff;
                color: #0f1125;
                text-align: left;
                font-weight: bold;
            }
            .styled-table th, .styled-table td {
                padding: 12px 15px;
            }
            .styled-table tbody tr {
                border-bottom: 1px solid #334466;
                transition: all 0.2s ease;
            }
            .styled-table tbody tr:nth-of-type(even) {
                background-color: rgba(255, 255, 255, 0.02);
            }
            .styled-table tbody tr:last-of-type {
                border-bottom: 2px solid #00d2ff;
            }
            .styled-table tbody tr:hover {
                background-color: rgba(0, 210, 255, 0.1);
                color: #fff;
            }
            
            /* Status Badge */
            .status-badge {
                background: linear-gradient(90deg, #00d2ff, #00ff9d);
                color: #0f1125;
                padding: 4px 10px;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: 700;
                box-shadow: 0 0 10px rgba(0, 210, 255, 0.4);
            }
            
            .metric-val {
                font-family: monospace;
                color: #00ff9d;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="perf-header">⚡ Model Performance Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-panel">
        <h3 style="color: #00d2ff; margin-bottom: 1rem;">📋 Detailed Performance Metrics</h3>
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Model Name</th>
                    <th>Accuracy</th>
                    <th>F1-Score</th>
                    <th>Recall</th>
                    <th>Precision</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Gradient Boosting Classifier</td>
                    <td class="metric-val">97.4%</td>
                    <td class="metric-val">97.7%</td>
                    <td class="metric-val">98.9%</td>
                    <td class="metric-val">96.6%</td>
                    <td><span class="status-badge">SELECTED</span></td>
                </tr>
               <tr>
                    <td>XGBoost Classifier</td>
                    <td class="metric-val">97.1%</td>
                    <td class="metric-val">97.4%</td>
                    <td class="metric-val">98.3%</td>
                    <td class="metric-val">96.5%</td>
                    <td><span class="status-badge">SELECTED</span></td>
                </tr>
                <tr>
                    <td>Multi-layer Perceptron</td>
                    <td class="metric-val">96.9%</td>
                    <td class="metric-val">98.9%</td>
                    <td class="metric-val">98.2%</td>
                    <td class="metric-val">96.3%</td>
                    <td><span class="status-badge">SELECTED</span></td>
                </tr>
                 <tr>
                    <td>Random Forest</td>
                    <td class="metric-val">96.7%</td>
                    <td class="metric-val">97.1%</td>
                    <td class="metric-val">97.4%</td>
                    <td class="metric-val">96.7%</td>
                    <td><span style="color: #666;">-</span></td>
                </tr>
                <tr>
                    <td>Support Vector Machine</td>
                    <td class="metric-val">96.4%</td>
                    <td class="metric-val">96.8%</td>
                    <td class="metric-val">98.0%</td>
                    <td class="metric-val">95.7%</td>
                    <td><span style="color: #666;">-</span></td>
                </tr>
                <tr>
                    <td>Decision Tree</td>
                    <td class="metric-val">96.0%</td>
                    <td class="metric-val">96.4%</td>
                    <td class="metric-val">96.1%</td>
                    <td class="metric-val">96.7%</td>
                    <td><span style="color: #666;">-</span></td>
                </tr>
                <tr>
                    <td>K-Nearest Neighbors</td>
                    <td class="metric-val">93.8%</td>
                    <td class="metric-val">94.4%</td>
                    <td class="metric-val">94.7%</td>
                    <td class="metric-val">94.2%</td>
                    <td><span style="color: #666;">-</span></td>
                </tr>
                <tr>
                    <td>Logistic Regression</td>
                    <td class="metric-val">93.4%</td>
                    <td class="metric-val">94.1%</td>
                    <td class="metric-val">95.3%</td>
                    <td class="metric-val">93.0%</td>
                    <td><span style="color: #666;">-</span></td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-panel" style="text-align: center;">
        <h3 style="color: #00d2ff; margin-bottom: 2rem;">🎯 Confusion Matrices - Top 3 Models</h3>
    """, unsafe_allow_html=True)
    
    # Needs to be outside HTML block for Streamlit widgets
    col1, col2, col3 = st.columns(3)
    
    def create_cm(title, vals):
        z = [[vals[0], vals[1]], [vals[2], vals[3]]]
        x = ['Phish', 'Safe']
        y = ['Phish', 'Safe']
        
        fig = go.Figure(data=go.Heatmap(
            z=z, x=x, y=y,
            colorscale=[[0, '#0A0B1A'], [1, '#00d2ff']],
            text=z, texttemplate="%{text}", textfont={"size": 16, "color": "white"},
            showscale=False
        ))
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(color="#fff", size=14)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#aaa"),
            width=250, height=250,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        return fig

    with col1:
        st.plotly_chart(create_cm("Gradient Boosting", [933, 43, 14, 1221]), use_container_width=True)
    with col2:
        st.plotly_chart(create_cm("XGBoost", [932, 44, 21, 1214]), use_container_width=True)
    with col3:
        st.plotly_chart(create_cm("MLP", [929, 47, 22, 1213]), use_container_width=True)
        
    st.markdown("</div>", unsafe_allow_html=True) # Close glass panel

def render_charts():
    render_navbar()
    
    # Custom CSS for Charts Page
    st.markdown("""
        <style>
            .charts-header {
                text-align: center;
                font-size: 2.5rem;
                font-weight: 700;
                color: #fff;
                margin-bottom: 2rem;
                text-shadow: 0 0 20px rgba(0, 210, 255, 0.5);
            }
            .glass-card {
                background: rgba(15, 17, 37, 0.7);
                border: 1px solid rgba(0, 210, 255, 0.2);
                border-radius: 20px;
                padding: 1.5rem;
                box-shadow: 0 0 30px rgba(0,0,0,0.4);
                margin-bottom: 2rem;
                transition: transform 0.3s ease;
            }
            .glass-card:hover {
                border-color: rgba(0, 210, 255, 0.5);
                transform: translateY(-5px);
            }
            .chart-title {
                color: #00d2ff;
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 1rem;
                text-align: center;
                letter-spacing: 1px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="charts-header">📊 Model Performance Analytics</div>', unsafe_allow_html=True)
    
    models = ["Gradient Boosting", "MLP", "XGBoost", "Random Forest", "SVM", "Decision Tree", "KNN", "Logistic Regression", "Naive Bayes"]
    acc = [97.4, 96.9, 97.1, 96.7, 96.4, 96.0, 93.8, 93.4, 60.5]
    f1 = [97.7, 98.9, 97.4, 97.1, 96.8, 96.4, 94.4, 94.1, 45.4]
    
    # Top Row: Bar Charts in Glass Cards
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown('<div class="glass-card"><div class="chart-title">🏆 Accuracy Comparison</div>', unsafe_allow_html=True)
        # Custom Color Scale: Cyan to Blue
        fig_acc = px.bar(x=models, y=acc, color=acc, 
                        color_continuous_scale=[[0, '#0055ff'], [1, '#00d2ff']])
        fig_acc.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="#aaa"),
            margin=dict(l=20, r=20, t=10, b=20),
            coloraxis_showscale=False,
            height=350,
            xaxis=dict(showgrid=False, title=None, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title=None)
        )
        fig_acc.update_traces(marker_line_width=0, opacity=0.9)
        st.plotly_chart(fig_acc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card"><div class="chart-title">💠 F1-Score Comparison</div>', unsafe_allow_html=True)
        # Custom Color Scale: Green to Emerald
        fig_f1 = px.bar(x=models, y=f1, color=f1, 
                       color_continuous_scale=[[0, '#008855'], [1, '#00ff9d']])
        fig_f1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="#aaa"),
            margin=dict(l=20, r=20, t=10, b=20),
            coloraxis_showscale=False,
            height=350,
            xaxis=dict(showgrid=False, title=None, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title=None)
        )
        fig_f1.update_traces(marker_line_width=0, opacity=0.9)
        st.plotly_chart(fig_f1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Row: Line Chart in Full Width Glass Card
    st.markdown('<div class="glass-card"><div class="chart-title">📈 Overall Metrics Trend</div>', unsafe_allow_html=True)
    
    x_line = models
    fig_line = go.Figure()
    
    # Glowing Lines
    fig_line.add_trace(go.Scatter(
        x=x_line, y=acc, mode='lines+markers', name='Accuracy',
        line=dict(color='#00d2ff', width=3, shape='spline'),
        marker=dict(size=8, color='#00d2ff', line=dict(width=2, color='white'))
    ))
    fig_line.add_trace(go.Scatter(
        x=x_line, y=f1, mode='lines+markers', name='F1-Score',
        line=dict(color='#00ff9d', width=3, shape='spline'),
        marker=dict(size=8, color='#00ff9d', line=dict(width=2, color='white'))
    ))
    
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color="#aaa"),
        height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="x unified",
        xaxis=dict(showgrid=False, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ROUTING ----------------
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'login':
    render_login()
elif st.session_state['page'] == 'dashboard':
    if not st.session_state['auth']: navigate_to('login')
    if not st.session_state['auth']: navigate_to('login')
    else: render_dashboard()
elif st.session_state['page'] == 'dataset_overview':
    if not st.session_state['auth']: navigate_to('login')
    else: render_dataset_overview()
elif st.session_state['page'] == 'scanner':
    if not st.session_state['auth']: navigate_to('login')
    else: render_scanner()
elif st.session_state['page'] == 'performance':
    if not st.session_state['auth']: navigate_to('login')
    else: render_performance()
elif st.session_state['page'] == 'charts':
    if not st.session_state['auth']: navigate_to('login')
    else: render_charts()
