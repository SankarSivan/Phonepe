import streamlit as st
import pyodbc

# ------------------------ Streamlit Config ----------------------------- #
st.set_page_config(
    page_title="PhonePe Dashboard", 
    #layout='wide',
    initial_sidebar_state="auto")

st.title("📊 PhonePe Pulse EDA Report")
st.subheader("Explore transaction data, user statistics, and geographical insights.")