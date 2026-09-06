import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Synthetic training data (simulates real click behavior)
data = pd.DataFrame({
    "clicks_per_ip": [1, 2, 3, 15, 20, 30, 1, 25],
    "time_gap": [120, 90, 60, 1, 0.5, 0.2, 200, 0.1],
    "hour": [10, 14, 16, 2, 3, 1, 11, 0],
    "referrer_missing": [0, 0, 0, 1, 1, 1, 0, 1],
    "fraud": [0, 0, 0, 1, 1, 1, 0, 1]
})

X = data.drop("fraud", axis=1)
y = data["fraud"]

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "fraud_model.pkl")

print("✅ Fraud detection model trained and saved")
