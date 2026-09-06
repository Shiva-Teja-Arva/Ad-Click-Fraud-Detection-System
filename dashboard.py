import streamlit as st
import pandas as pd
import time
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Real-Time Click Fraud Monitoring Dashboard")

LOG_FILE = "click_logs.csv"

refresh_rate = st.sidebar.slider("Refresh seconds", 1, 10, 3)

while True:
    try:
        df = pd.read_csv(LOG_FILE)
    except:
        st.warning("No log file found yet.")
        time.sleep(refresh_rate)
        continue

    if df.empty:
        st.info("No clicks recorded yet.")
        time.sleep(refresh_rate)
        continue

    # ---- Metrics ----
    total_clicks = len(df)
    fraud_count = df["fraud"].sum()
    fraud_rate = fraud_count / total_clicks * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clicks", total_clicks)
    col2.metric("Fraud Clicks", fraud_count)
    col3.metric("Fraud Rate %", round(fraud_rate, 2))

    # ---- Real-Time Alert ----
    if fraud_count > 0:
        st.error("⚠️ Fraud clicks detected!")

    # ---- Clicks per IP ----
    ip_counts = df["ip"].value_counts().reset_index()
    ip_counts.columns = ["ip", "clicks"]

    fig_ip = px.bar(ip_counts.head(10),
                    x="ip",
                    y="clicks",
                    title="Top IP Click Activity")

    st.plotly_chart(fig_ip, use_container_width=True)

    # ---- Time Gap Anomaly Chart ----
    fig_gap = px.scatter(df,
                         x=df.index,
                         y="time_gap",
                         color="fraud",
                         title="Click Time Gap Anomaly Detection")

    st.plotly_chart(fig_gap, use_container_width=True)

    # ---- Fraud Probability Chart ----
    fig_prob = px.line(df,
                       y="fraud_probability",
                       title="Fraud Probability Trend")

    st.plotly_chart(fig_prob, use_container_width=True)

    time.sleep(refresh_rate)
    st.rerun()
