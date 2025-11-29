import streamlit as st 

import streamlit as st
import json
import asyncio
from groq_utils import email_structure, get_email_attributes
# Title
st.title("Email Attribute visualizer")

# Inputs
subject = st.text_input("Email Subject")
body = st.text_area("Email Body")

# Button to visualize JSON
if st.button("Show JSON"):
    email = email_structure.format(subject=subject,body=body)
    result_json = asyncio.run(get_email_attributes(email))
    st.json(result_json)

