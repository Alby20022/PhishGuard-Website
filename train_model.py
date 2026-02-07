import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("Loading dataset...")

# Load dataset
data = pd.read_csv("phishing.csv")

# Features & label
X = data.drop("Result", axis=1)
y = data["Result"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training model...")

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# Accuracy
accuracy = accuracy_score(y_test, model.predict(X_test))
print("Accuracy:", accuracy)

# SAVE MODEL AS model1.pkl
with open("model1.pkl", "wb") as f:
    pickle.dump(model, f)

print("model1.pkl created successfully ✅")
