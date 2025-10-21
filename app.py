import streamlit as st
from openai import OpenAI
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title
st.set_page_config(page_title="EcoBot", page_icon="🌿")
st.title("🌿 EcoBot — Your School’s Sustainability Assistant")

# Sidebar
st.sidebar.header("Eco Insights")
st.sidebar.info("💡 Tip of the Day: Turn off lights when leaving a classroom!")

# Tabs for Chat and Dashboard
tab1, tab2 = st.tabs(["💬 Chat", "📊 Dashboard"])

# Initialize session history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CHAT TAB ---
with tab1:
    st.subheader("Ask EcoBot Anything!")
    user_input = st.text_input("You:", "")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Send message to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are EcoBot, a friendly sustainability assistant."},
                {"role": "user", "content": suggestion_prompt}
            ]
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # Display
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

    # Add AI-generated suggestion
    # Always create a fresh messages list for this call
    dashboard_prompt = f"The school's paper usage data is as follows: Jan=250kg, Feb=230kg, Mar=220kg, Apr=200kg, May=210kg, Jun=190kg. Suggest one sustainability improvement."

    dashboard_messages = [
        {"role": "system", "content": "You are EcoBot, a friendly sustainability assistant."},
        {"role": "user", "content": dashboard_prompt}
    ]

    suggestion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=dashboard_messages
    )

    st.success("🧠 EcoBot Suggests: " + suggestion.choices[0].message.content)
