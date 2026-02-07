# 🛡️ PhishGuard - Advanced AI Phishing Detection

PhishGuard is a sophisticated cybersecurity tool designed to detect phishing URLs using Machine Learning. It analyzes URL patterns, structure, and content to determine if a website is safe or malicious, providing real-time protection and detailed risk analysis.

## ✨ Key Features

- **🚀 AI-Based Detection**: Uses a Random Forest Classifier trained on a balanced dataset of safe and phishing URLs.
- **🔍 Detailed Risk Analysis**: Breaks down *why* a site is flagged (e.g., suspicious length, IP usage, masking, etc.).
- **⚠️ Caution System**: Flags ambiguous or low-confidence URLs with a warning, allowing users to proceed at their own risk.
- **✅ Smart Whitelisting**: Automatically trusts known safe domains (Google, Govt, Banking sites) to prevent false positives.
- **📊 Real-time Dashboard**: Tracks scan history and outcomes in a live activity log.
- **🔒 Secure Architecture**: Built with Streamlit and optimized for speed and accuracy.

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (Python-based Web Framework)
- **Machine Learning**: Scikit-learn (Random Forest)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Language**: Python 3.x

## 🚀 Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Alby20022/PhishGuard-Website.git
    cd PhishGuard-Website
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    streamlit run streamlit_app.py
    ```

4.  **Access the Dashboard**:
    Open your browser and navigate to `http://localhost:8501`.

## 📂 Project Structure

- `streamlit_app.py`: Main application code (UI & Logic).
- `model1.pkl`: Pre-trained Machine Learning model.
- `phishing.csv`: Dataset used for training.
- `train_model.py`: Script to retrain the model with new data.
- `add_data.py`: Utility to add new URLs to the dataset.
- `verify_model.py`: Script to verify model accuracy.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---
*Built with ❤️ for a safer internet.*
