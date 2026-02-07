"""
Legacy Flask application.
Streamlit is used as the final interface.
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask version (deprecated). Use Streamlit UI."

if __name__ == "__main__":
    app.run()
