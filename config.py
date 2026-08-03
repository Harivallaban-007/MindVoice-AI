import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        api_key = st.secrets["GROQ_API_KEY"]

    return api_key