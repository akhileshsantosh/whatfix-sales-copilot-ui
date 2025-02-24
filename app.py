import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Backend API URL
BACKEND_API_URL = "https://whatfix-sales-copilot-backend.onrender.com"

# Streamlit UI Styling
st.set_page_config(page_title="Whatfix Salesforce Copilot", layout="wide")

st.markdown("""
    <style>
        h1 {
            text-align: center; 
            font-size: 40px; 
            font-weight: bold; 
            color: #333;
        }
        .prompt-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .prompt-button {
            width: 220px;
            height: 150px;
            padding: 20px;
            border-radius: 20px; 
            font-size: 18px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 2px solid #007bff;
            background-color: white;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .prompt-button:hover {
            background-color: #007bff;
            color: white;
        }
        .response-box { 
            background-color: #eef2f7; 
            padding: 15px; 
            border-radius: 10px; 
            margin-top: 10px; 
            border-left: 5px solid #007bff; 
        }
        .sidebar-title { 
            font-size:18px; 
            font-weight: bold; 
            margin-bottom:10px; 
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1>🚀 Whatfix Salesforce Copilot</h1>", unsafe_allow_html=True)

# Sidebar: Select User
st.sidebar.markdown("<p class='sidebar-title'>👤 Select a Sales User</p>", unsafe_allow_html=True)
users = requests.get(f"{BACKEND_API_URL}/users").json()
user_options = {user["Name"]: user["Id"] for user in users}
selected_user = st.sidebar.selectbox("Choose User", list(user_options.keys()))

st.subheader(f"🤖 Copilot for {selected_user}")

# Initialize response storage
if "responses" not in st.session_state:
    st.session_state.responses = []

# Prompt Buttons as a Grid
st.markdown('<div class="prompt-container">', unsafe_allow_html=True)

if st.button("📂 Get Open Opportunities", key="open_opportunities"):
    response = requests.get(f"{BACKEND_API_URL}/opportunities/open?user_id={user_options[selected_user]}")
    data = response.json()
    
    if data:
        response_text = "**Here are the open opportunities:**\n\n"
        for i, opp in enumerate(data, 1):
            response_text += f"{i}. **{opp['Name']}**\n   - Amount: {opp.get('Amount', 'N/A')}\n   - Stage: {opp['StageName']}\n   - Close Date: {opp['CloseDate']}\n\n"
    else:
        response_text = "No open opportunities found."

    st.session_state.responses.append(response_text)

if st.button("📝 Summarize Opportunity", key="summarize_opportunity"):
    opportunity_id = st.text_input("Enter Opportunity ID:")
    if opportunity_id:
        response = requests.get(f"{BACKEND_API_URL}/opportunities/summarize?opportunity_id={opportunity_id}")
        summary = response.json().get("summary", "No summary available.")
        st.session_state.responses.append(f"**Opportunity Summary:**\n\n{summary}")

if st.button("📒 Get Notes & Attachments", key="get_notes"):
    response = requests.get(f"{BACKEND_API_URL}/opportunities/details?user_id={user_options[selected_user]}")
    notes = response.json().get("notes", "No notes available.")
    st.session_state.responses.append(f"**Notes & Attachments:**\n\n{notes}")

if st.button("📞 Summarize Calls", key="summarize_calls"):
    response = requests.get(f"{BACKEND_API_URL}/opportunities/calls?user_id={user_options[selected_user]}")
    call_summary = response.json().get("summary", "No call summary available.")
    st.session_state.responses.append(f"**Call Summary:**\n\n{call_summary}")

st.markdown('</div>', unsafe_allow_html=True)

# Display previous responses
if st.session_state.responses:
    st.subheader("📌 Previous Responses")
    for response in st.session_state.responses:
        st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

# Chat Interface
st.subheader("💬 Chat with Copilot")
user_query = st.text_input("Ask a question:")

if user_query:
    response = requests.get(f"{BACKEND_API_URL}/chat?question={user_query}")
    chat_response = response.json().get("response", "No response available.")
    st.session_state.responses.append(f"**User Query:** {user_query}\n\n**Copilot Response:**\n\n{chat_response}")
