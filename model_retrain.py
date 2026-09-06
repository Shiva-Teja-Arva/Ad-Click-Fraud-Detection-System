import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load real click data
df = pd.read_csv("click_logs.csv")

# Use ONLY columns that exist
features = [
    "clicks_per_ip",
    "time_gap",
    "hour",
    "referrer_missing"
]

# Simple heuristic labeling (temporary but valid)
df["fraud_label"] = (
    (df["clicks_per_ip"] > 10) &
    (df["time_gap"] < 1)
).astype(int)

X = df[features]
y = df["fraud_label"]

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X, y)

# Save updated model
joblib.dump(model, "fraud_model.pkl")

print("✅ Model retrained successfully using available features")
