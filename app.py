import streamlit as st
from openai import OpenAI
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="EcoBot", page_icon="🌿")
st.title("🌱 EcoBot — Your School Sustainability Assistant")

print(st.secrets["OPENAI_API_KEY"][:8] + "...")

"""

# Sidebar with daily tip
print("Initializing eco_tip...")
if "eco_tip" not in st.session_state:
    st.session_state.eco_tip = random.choice([
        "💧 Turn off taps tightly after use",
        "🌿 Bring reusable bottles instead of plastic ones",
        "💡 Use natural light whenever possible",
        "📄 Print double-sided to save paper"
    ])

st.sidebar.header("Eco Tip of the Day")
st.sidebar.info(st.session_state.eco_tip)

# Tabs
tab1, tab2 = st.tabs(["💬 Chat", "📊 Dashboard"])

# --- CHAT TAB ---
# --- CHAT TAB ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

with tab1:
    user_input = st.text_input(
        "Ask EcoBot about sustainability:",
        value=st.session_state.user_input,
        key="user_input"
    )
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are EcoBot, a friendly AI helping the school become more sustainable."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.markdown(f"**EcoBot:** {reply}")
        
        # Log to CSV
        with open("chat_log.csv", "a") as f:
            f.write(f"{datetime.now()},{user_input},{reply}\n")
# --- DASHBOARD TAB ---
with tab2:
    st.subheader("📈 School Eco Data (Mock)")
    data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Paper Usage (kg)": [250, 230, 220, 200, 210, 190]
    })
    fig = px.line(data, x="Month", y="Paper Usage (kg)", title="Paper Usage Trend")
    st.plotly_chart(fig)

    # AI suggestion (simplified text)
    dashboard_prompt = "The school's paper usage for 6 months: Jan=250kg, Feb=230kg, Mar=220kg, Apr=200kg, May=210kg, Jun=190kg. Suggest one simple eco-friendly improvement."
    
    dashboard_messages = [
        {"role": "system", "content": "You are EcoBot, a friendly sustainability assistant."},
        {"role": "user", "content": dashboard_prompt}
    ]
    
    try:
        suggestion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=dashboard_messages
        )
        st.success("🧠 EcoBot Suggests: " + suggestion.choices[0].message.content)
    except Exception as e:
        st.error(f"Error fetching EcoBot suggestion: {e}")

"""
