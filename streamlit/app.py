import os
import requests
import streamlit as st

API = os.getenv("API_URL", "http://api:8000")  # use service name 'api' from compose

st.set_page_config(page_title="MyApp Streamlit Client", layout="centered")
st.title("MyApp — Streamlit Client")

st.subheader("Recent Values")
if st.button("Refresh values"):
    try:
        values = requests.get(f"{API}/values?limit=20", timeout=10).json()
        st.table(values)
    except Exception as e:
        st.error(f"Error: {e}")

# Health check
st.subheader("API Health")
try:
    health = requests.get(f"{API}/health", timeout=5).json()
    st.success(health)
except Exception as e:
    st.error(f"Cannot reach API at {API}: {e}")

# Compute average
st.subheader("Compute Average")
if st.button("Get average"):
    try:
        avg = requests.get(f"{API}/compute", timeout=10).json()
        st.info(avg)
    except Exception as e:
        st.error(f"Error: {e}")

# Insert value
st.subheader("Insert a Value")
val = st.number_input("Value", value=42.0, step=1.0)
if st.button("Insert"):
    try:
        r = requests.post(f"{API}/insert/{val}", timeout=10).json()
        st.success(r)
        # refresh average
        avg = requests.get(f"{API}/compute", timeout=10).json()
        st.write("New average:", avg)
    except Exception as e:
        st.error(f"Error: {e}")

st.caption(f"API URL: {API}")