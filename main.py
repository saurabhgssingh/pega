import asyncio
import time
import os
import streamlit as st
from dotenv import load_dotenv

AUTO_REFRESH_INTERVAL = 10   # seconds
load_dotenv()

os.environ["EMAIL_PASSWORD"] = st.secrets["EMAIL_PASSWORD"]
os.environ["EMAIL_USERNAME"] = st.secrets["EMAIL_USERNAME"]
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]



pages = [
        st.Page(r"app\pages\manual_test.py", title="Test Manually"),
        st.Page(r"app\pages\dashboard.py", title="Dashboard")
]

pg = st.navigation(pages)
pg.run()