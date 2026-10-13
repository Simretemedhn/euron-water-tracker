import streamlit as st
import requests

st.set_page_config(page_title="Euron Water Tracker", page_icon="💧", layout="centered")

API_URL = "http://127.0.0.1:8000"

st.title("💧 Euron AI Agent for Tracking Daily Water Intake")
st.write("Monitor your daily hydration and receive AI-powered feedback instantly!")

user_id = st.sidebar.text_input("User ID", value="user_123")

st.header("Log Water Intake")
amount = st.number_input("Enter water amount (ml):", min_value=0.0, step=100.0)

if st.button("Submit Intake"):
    if amount > 0:
        payload = {"user_id": user_id, "amount_ml": amount}
        try:
            res = requests.post(f"{API_URL}/log-water/", json=payload)
            if res.status_code == 200:
                st.success("Successfully logged water intake!")
            else:
                st.error("Failed to log intake on the backend.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI backend. Ensure it is running!")
    else:
        st.warning("Please enter a valid amount greater than 0.")

st.markdown("---")
st.header("📊 Hydration Status & AI Feedback")

if st.button("Get AI Feedback & Stats"):
    try:
        res = requests.get(f"{API_URL}/feedback/{user_id}")
        if res.status_code == 200:
            data = res.json()
            st.metric(label="Total Intake Today (ml)", value=f"{data['total_intake_ml']} ml")
            st.info(f"**AI Agent Feedback:**\n\n{data['feedback']}")
        else:
            st.error("Could not fetch feedback.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI backend.")