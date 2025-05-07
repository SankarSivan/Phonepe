import streamlit as st
import pyodbc

# Streamlit Config
st.set_page_config(
    page_title="PhonePe KPI Dashboard",
    layout="wide"
)

# Title
st.title("📊 PhonePe Dashboard")
st.markdown("Showing key metrics from PhonePe data")

# Database Connection
server = 'WLE2478W'
database = 'phonepe'
username = 'sa'
password = 'Thought@12345'

try:
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()

    # Layout for 2 KPI cards
    col1, col2 = st.columns(2)

    with col1:
        cursor.execute("SELECT SUM(Transaction_amount) FROM aggr_trans")
        total_amount = cursor.fetchone()[0] or 0
        st.metric("💸 Total Payment Value (₹ Cr)", f"{total_amount / 1e7:,.2f}")

    with col2:
        cursor.execute("SELECT SUM(Transaction_count) FROM aggr_trans")
        total_count = cursor.fetchone()[0] or 0
        st.metric("📦 Total Payment Count", f"{total_count:,}")

except pyodbc.Error as e:
    st.error(f"Database connection failed: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
