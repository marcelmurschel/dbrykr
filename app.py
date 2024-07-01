import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your custom pages
from base import base_page
from expenses_tracker import expenses_tracker_page
from price_scraper import price_scraper_page
from interview_bot import interview_bot_page

# Set your OpenAI and Anthropic API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ASSISTANT_ID"] = os.getenv("ASSISTANT_ID")

# Initialize session state for the custom variable name
if 'custom_var_name' not in st.session_state:
    st.session_state.custom_var_name = "Q10"

# Sidebar for navigation
st.sidebar.title("🧪 debruyker lab")
page = st.sidebar.radio("Go to", [
    "🏠 BASE",
    "💸 Expenses Tracker",
    "🔍 Price Scraper",
    "🎙️ Interview Bot"
])

# Navigation
if page == "🏠 BASE":
    base_page()
elif page == "💸 Expenses Tracker":
    expenses_tracker_page()
elif page == "🔍 Price Scraper":
    price_scraper_page()
elif page == "🎙️ Interview Bot":
    interview_bot_page()

# Footer
st.write("\n\n")
st.markdown("<div style='color: grey; text-align: center;'>🤖 made by debruyker lab</div>", unsafe_allow_html=True)
