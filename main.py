from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import pandas as pd
import joblib
from datetime import datetime
import os
from urllib.parse import urlparse



from feature_engine import extract_features

app = FastAPI(title="Global Click Fraud Detection System")

MODEL_PATH = "fraud_model.pkl"
LOG_FILE = "click_logs.csv"
EXCEL_FILE = "click_logs.xlsx"

model = joblib.load(MODEL_PATH)

@app.get("/track")
async def track_click(request: Request, url: str):
    ip = request.client.host
    headers = request.headers

    user_agent = headers.get("user-agent", "")
    referrer = headers.get("referer", "")

    # --- URL VALIDATION ---
    parsed = urlparse(url)

    if not parsed.scheme or not parsed.netloc:
        return {
            "status": "error",
            "message": "Invalid URL format. Must include http/https."
        }
# ----------------------

    # Extract behavioral features
    features = extract_features(ip, referrer)

    df = pd.DataFrame([features])
    probs = model.predict_proba(df)[0]

# If model learned only ONE class
    if len(probs) == 1:
        fraud_prob = 0.0
    else:
        fraud_prob = probs[1]


    # Rule-based fraud signals (strong indicators)
    rule_fraud = (
        features["clicks_per_ip"] > 10 and
        features["time_gap"] < 1
    )

    # ML probability (safe)
    fraud = int(rule_fraud or fraud_prob > 0.6)


    log_row = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip,
        "url": url,
        "user_agent": user_agent,
        "fraud_probability": round(fraud_prob, 4),
        "fraud": fraud,
        **features
    }

    log_df = pd.DataFrame([log_row])

    if os.path.exists(LOG_FILE):
        log_df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        log_df.to_csv(LOG_FILE, index=False)

    # Auto-sync to Excel
    try:
        pd.read_csv(LOG_FILE).to_excel(EXCEL_FILE, index=False)
    except PermissionError:
        pass


    # Redirect if legit, block if fraud (configurable)
    if fraud:
        return JSONResponse(
            status_code=403,
            content={"message": "Fraudulent click detected", "score": fraud_prob}
        )

    return {
    "status": "ok",
    "redirect_to": url,
    "fraud_probability": fraud_prob,
    "fraud": fraud,
    "features": features
}

