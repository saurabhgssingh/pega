import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
from app.db_utils import load_data
from app.email_utils import start_listening
import asyncio
st.set_page_config(page_title="Incident Command Center", layout="wide")

auto_refresh = True
# Sidebar for Controls
# Main Title
st.title("📊 Customer Incident Dashboard")
st.markdown("Real-time monitoring of incoming support tickets and email intents.")

# Create a placeholder for the entire dashboard content
# This allows us to overwrite the UI on every refresh cycle without duplicating elements
dashboard_placeholder = st.empty()

def render_dashboard():
    """Function to render the UI elements"""
    df = load_data()

    with dashboard_placeholder.container():
        # --- Top KPIs ---
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            st.metric(label="Total Incidents", value=len(df))
        with kpi2:
            top_intent = df['intent'].mode()[0] if not df.empty else "N/A"
            st.metric(label="Top Issue Category", value=top_intent)
        with kpi3:
            unique_products = df['product'].nunique()
            st.metric(label="Active Products", value=unique_products)
        with kpi4:
            # Simulate a "Live" status
            st.metric(label="System Status", value="Online 🟢")

        st.divider()

        # --- Visualizations ---
        col1, col2 = st.columns(2)

        st.subheader("Intent Analysis")
        if not df.empty:
            # Count incidents by intent
            intent_counts = df['intent'].value_counts().reset_index()
            intent_counts.columns = ['intent', 'count']
            fig_intent = px.bar(intent_counts, x='count', y='intent', orientation='h', 
                                title='Volume by Issue Type', color='count')
            st.plotly_chart(fig_intent, use_container_width=True)
        else:
            st.info("No data available.")

        # --- Data Table ---
        st.subheader("Recent Ticket Log")
        st.dataframe(
            df[['id', 'incident_time','customer_name', 'product', 'intent', 'requested_action']],
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# 4. EXECUTION LOOP
# ==========================================

# if auto_refresh:
#     # If auto-refresh is on, we run a loop
#     # Note: In a real production app, st.rerun() is often preferred over while loops,
#     # but a loop with empty() is fine for simple dashboards.
#     while True:
#         render_dashboard()
#         asyncio.run(start_listening())
#         time.sleep(10) # Refresh every 10 seconds
# else:
#     # Static render
#     render_dashboard()