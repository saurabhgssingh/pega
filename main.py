import asyncio
import time
import streamlit as st
from dotenv import load_dotenv
from app.main import render_dashboard
from app.email_utils import start_listening

AUTO_REFRESH_INTERVAL = 10   # seconds
load_dotenv()
def main():
    # Run your dashboard content
    render_dashboard()

    # Run async email listener once per refresh cycle
    asyncio.run(start_listening())

    # Trigger auto-refresh
    st.query_params.from_dict({"tx":int(time.time())})  # forces URL change so Streamlit sees a state change
    # st.experimental_set_query_params(_=int(time.time()))  # forces URL change so Streamlit sees a state change
    time.sleep(AUTO_REFRESH_INTERVAL)
    st.rerun()   # re-run app


if __name__ == "__main__":
    main()
