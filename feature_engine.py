import time
from collections import defaultdict

# Stores click timestamps per IP
click_store = defaultdict(list)

def extract_features(ip: str, referrer: str):
    now = time.time()
    history = click_store[ip]

    clicks_per_ip = len(history) + 1

    if history:
        time_gap = now - history[-1]
    else:
        time_gap = 999  # first click looks human

    hour = time.localtime().tm_hour
    referrer_missing = 1 if not referrer else 0

    history.append(now)

    return {
        "clicks_per_ip": clicks_per_ip,
        "time_gap": round(time_gap, 3),
        "hour": hour,
        "referrer_missing": referrer_missing
    }
