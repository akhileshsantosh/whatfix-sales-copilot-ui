import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Backend API URL
BACKEND_API_URL = "https://whatfix-sales-backend.onrender.com"

# Streamlit UI Styling
st.set_page_config(page_title="Whatfix Salesforce Copilot", layout="wide")

st.markdown("""
    <style>
        .big-font { font-size:24px !important; }
        .small-text { font-size:16px; color:gray; }
        .stButton button { width: 100%; padding: 15px; border-radius: 10px; }
        .chat-box { background-color: #f3f3f3; padding: 10px; border-radius: 10px; }
        .sidebar-title { font-size:18px; font-weight: bold; margin-bottom:10px; }
    </style>
""", unsafe_allow_html=True)

st.image("https://upload.wikimedia.org/wikipedia/commons/2/28/Whatfix_logo.svg", width=200)
st.markdown("<h1 class='big-font'>🚀 Whatfix Salesforce Copilot</h1>", unsafe_allow_html=True)

# Sidebar: Select User
st.sidebar.markdown("<p class='sidebar-title'>👤 Select a Sales User</p>", unsafe_allow_html=True)
users = requests.get(f"{BACKEND_API_URL}/users").json()
user_options = {user["Name"]: user["Id"] for user in users}
selected_user = st.sidebar.selectbox("Choose User", list(user_options.keys()))

st.subheader(f"📊 Copilot for {selected_user}")

col1, col2 = st.columns(2)

with col1:
    if st.button("📂 Get Open Opportunities"):
        response = requests.get(f"{BACKEND_API_URL}/opportunities/open?user_id={user_options[selected_user]}")
        st.json(response.json())

    if st.button("📝 Summarize Opportunity"):
        opportunity_id = st.text_input("Enter Opportunity ID:")
        if st.button("Summarize"):
            response = requests.get(f"{BACKEND_API_URL}/opportunities/summarize?opportunity_id={opportunity_id}")
            st.write(response.json()["summary"])

with col2:
    if st.button("📒 Get Notes & Attachments"):
        response = requests.get(f"{BACKEND_API_URL}/opportunities/details?user_id={user_options[selected_user]}")
        st.json(response.json())

    if st.button("📞 Summarize Calls"):
        response = requests.get(f"{BACKEND_API_URL}/opportunities/calls?user_id={user_options[selected_user]}")
        st.write(response.json()["summary"])

# Chat Interface
st.subheader("💬 Chat with Copilot")
user_query = st.text_input("Ask a question:")
if st.button("🔎 Search"):
    response = requests.get(f"{BACKEND_API_URL}/chat?question={user_query}")
    st.markdown(f"<div class='chat-box'>{response.json()['response']}</div>", unsafe_allow_html=True)

