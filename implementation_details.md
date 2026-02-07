# Implementation Details

## 1. Module Implementation

### Frontend Module (`streamlit_app.py`)
The user interface is built using **Streamlit**, a Python framework for data apps. It utilizes a single-page application architecture with a simulated multi-page navigation system managed via `st.session_state`.

*   **Custom Styling**: Implements a "Dark Glassmorphism" aesthetic using global CSS injection (`st.markdown` with `<style>`). Key design elements include:
    *   Translucent backgrounds (`backdrop-filter: blur`).
    *   Neon accents (#00d2ff, #00ff9d).
    *   Customized standard widgets (Input fields, Buttons, File Uploader).
*   **Navigation**: A persistent side/top navbar that conditionally renders based on authentication state (`st.session_state['auth']`).
*   **Pages**:
    *   **Home/Login**: Entry point with authentication logic (currently hardcoded demo credentials).
    *   **Dashboard**: File upload interface with drag-and-drop functionality and dashed-border styling.
    *   **Dataset Overview**: Displays statistical metrics (Row/Column counts) and a data preview of uploaded CSVs using Pandas.
    *   **Scanner**: Real-time URL analysis interface where the user inputs a URL, and the system extracts features to predict its safety.

### Machine Learning Module (`train_model.py`)
Responsible for training the phishing detection model.
*   **Algorithm**: **Random Forest Classifier** (`sklearn.ensemble.RandomForestClassifier`).
*   **Features**: The model is trained on numerical features extracted from URLs (Length, Dot count, Hyphen count, etc.).
*   **Persistence**: The trained model is serialized and saved as `model1.pkl` using the `pickle` library, allowing the frontend to load it for inference without retraining.

### Data Management
*   **Session State**: The application uses Streamlit's Session State to persist data (e.g., `uploaded_df`, `auth_status`) across reruns while the user is active.
*   **Data Source**: `phishing.csv` is used as the training dataset.

## 2. Code Structure & Pseudo-Code

### Directory Structure
```
/root
├── streamlit_app.py  # Main Entry Point & UI
├── train_model.py    # Model Training Script
├── api.py            # API Endpoint (Placeholder)
├── phishing.csv      # Training Data (CSV)
└── model1.pkl        # Serialized Model
```

### Feature Extraction Logic (Pseudo-Code)
This logic exists in `streamlit_app.py` to transform raw URLs into the format expected by the model.

```python
FUNCTION extract_features(url):
    details = []
    details.append(LENGTH of url)
    details.append(COUNT of '.' in url)
    details.append(COUNT of '-' in url)
    details.append(COUNT of '@' in url)
    details.append(1 IF "https" in url ELSE 0)
    details.append(COUNT of digits in url)
    RETURN numpy_array(details)
```

### Inference Logic
```python
FUNCTION predict(url):
    # 1. Check Whitelist (optimization)
    IF url in safe_domains: RETURN Safe
    
    # 2. Check Blacklist (security)
    IF url in phish_domains: RETURN Phishing

    # 3. Model Prediction
    features = extract_features(url)
    prediction = model.predict(features)
    RETURN prediction
```

## 3. Data Flow & Pipelines

### Data Preprocessing & Training (`train_model.py`)
1.  **Ingestion**: Load `phishing.csv`.
2.  **Splitting**: Split data into Feature Matrix `X` (all columns except Result) and Target Vector `y` (Result).
3.  **Train/Test Split**: 80% Training, 20% Testing.
4.  **Training**: Fit Random Forest Classifier (100 estimators).
5.  **Evaluation**: Calculate accuracy on Test set.
6.  **Serialization**: Save object to `model1.pkl`.

### Testing Steps
*   **Unit Testing**: Manual validation of feature extraction logic.
*   **Model Validation**: Accuracy score printed during training execution.
*   **E2E Testing**: Manual verification via the "Scanner" page in the web app.

## 4. Hardware & IoT Setup
**Project Type**: Pure Software / Web Application.

*   **Sensors**: N/A (Input is user-provided text/URL).
*   **Actuators**: N/A.
*   **Hardware**: Runs on standard commodity hardware (Server/Local Machine) capable of running Python 3.x.
*   **Data Flow**:
    `User Input (Browser)` -> `Streamlit Server (Python)` -> `Model Inference` -> `Response (UI)`

*Note: There are no specific hardware sensors or IoT device integrations required for this specific implementation of the URL detection system.*
