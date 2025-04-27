# PhonePe Pulse Dashboard
import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px
import json
import requests

# ------------------------ Streamlit Config ----------------------------- #
st.set_page_config(
    page_title="PhonePe Dashboard", 
    layout='wide',
    initial_sidebar_state="auto")

def set_bg_color(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Example usage:
set_bg_color('#e6ffe6') # Light green

st.title("My Streamlit App")
st.write("This app has a custom background color.")


# ------------------------- MySQL DB Connection ------------------------- #
conn = mysql.connector.connect(
    host="b0qbqnddydban6etyumx-mysql.services.clever-cloud.com",
    user="ua3wnbdcxwjeyr9w",
    password="B7kTGpzaoxHbTN9DznoT",
    database="b0qbqnddydban6etyumx"
)
cursor = conn.cursor()


# ------------------------ Title ----------------------------- #
# Title in the first row
st.title("📊 PhonePe Pulse EDA Report")
st.subheader("Explore transaction data, user statistics, and geographical insights.")

# ------------------------ Button Layout ----------------------------- #
# Initialize session state for button tracking
if 'active_button' not in st.session_state:
    st.session_state.active_button = 'about' # Default on first load
    
# Three buttons in the second row (horizontal layout)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📈 About", use_container_width=True):
        st.session_state.active_button = 'about'

with col2:
    if st.button("📊 Payments", use_container_width=True):
        st.session_state.active_button = 'payments'

with col3:
    if st.button("📱 Insurance", use_container_width=True):
        st.session_state.active_button = 'insurance'

with col4:
    if st.button(":male-scientist: User", use_container_width=True):
        st.session_state.active_button = 'User'

with col5:
    if st.button("🗺️ Geographical", use_container_width=True):
        st.session_state.active_button = 'geo'

# ------------------------------ About --------------------------------------- #
if st.session_state.active_button == 'about':
    st.title("📈 PhonePe Transaction Insights - About Page")

    # About Section
    st.header("🔍 About")
    st.markdown("""
    **PhonePe Transaction Insights** is a data-driven analytics project built on top of the 
    publicly available **PhonePe Pulse** data platform.  
    The goal is to analyze and visualize payment transaction trends, insurance adoption, 
    and user engagement across different states, districts, and pin codes of India.  
    The platform uses advanced SQL queries, Python (Streamlit), and interactive dashboards
    to deliver critical insights for the Finance/Payment Systems domain.
    """)

    # Business Problem Section
    st.header("💼 Business Problem")
    st.markdown("""
    Digital payment systems like PhonePe are growing exponentially. However, businesses, 
    marketers, and product teams lack actionable insights into:
    
    - Customer segmentation based on transaction patterns
    - Identifying geographical strongholds and weak spots
    - Detecting potential fraud patterns
    - Tracking user engagement and insurance service adoption
    - Benchmarking against competitor platforms
    """)

    # Approach Section
    st.header("🛠 Approach")
    st.markdown("""
    - **Data Extraction**: Collected aggregated transaction, insurance, and user datasets from PhonePe Pulse APIs.
    - **SQL Proficiency**: Used MySQL for heavy data aggregation and performance optimization.
    - **Analytical Thinking**: Designed KPIs, trend analyses, and comparative studies.
    - **Visualization**: Built dynamic, interactive dashboards using Streamlit and Plotly Express.
    - **Documentation**: Structured detailed project documentation for clarity and future improvements.
    """)

    # Business Value Section
    st.header("🚀 Business Value")
    st.markdown("""
    - **Customer Segmentation**: Drive more targeted marketing and personalized offers.
    - **Fraud Detection**: Early detection of abnormal transaction patterns.
    - **Geographical Insights**: Invest smartly in regions showing high potential.
    - **User Engagement Metrics**: Improve retention strategies based on behavioral patterns.
    - **Insurance Analysis**: Expand micro-insurance offerings through better targeting.
    - **Competitive Edge**: Benchmark performance to stay ahead in the digital payments race.
    """)

# ------------------------- Key KPI Metrics ------------------------- #
    st.subheader("📊 Key KPI Metrics")
    # First row of metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        cursor.execute(f"SELECT SUM(Transaction_amount) FROM aggr_trans_data")
        total_amount = cursor.fetchone()[0] or 0
        st.metric("💸 Total Payment Value (₹ Cr)", f"{total_amount/1e7:,.2f}")

    with col2:
        cursor.execute(f"SELECT SUM(Transaction_count) FROM aggr_trans_data")
        total_count = cursor.fetchone()[0] or 0
        st.metric("📦 Total Payment Count ", f"{total_count:,}")

    with col3:
        cursor.execute(f"SELECT AVG(Transaction_amount) FROM aggr_trans_data")
        avg_amount = cursor.fetchone()[0] or 0
        st.metric("💰 Avg Payment Value (₹ Cr)", f"{avg_amount/1e7:,.2f}")
        
    # Second row of metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        cursor.execute(f"SELECT SUM(amount) FROM aggr_insurance_data")
        total_amount = cursor.fetchone()[0] or 0
        st.metric("💸 Total Insurance Value (₹ Cr)", f"{total_amount/1e7:,.2f}")

    with col2:
        cursor.execute(f"SELECT SUM(count) FROM aggr_insurance_data")
        total_count = cursor.fetchone()[0] or 0
        st.metric("📦 Total Insurance Count", f"{total_count:,}")

    with col3:
        cursor.execute(f"SELECT AVG(amount) FROM aggr_insurance_data")
        avg_amount = cursor.fetchone()[0] or 0
        st.metric("💰 Avg Insurance Value (₹ Cr)", f"{avg_amount/1e7:,.2f}")

# ------------------------- Payment Section ------------------------- #
elif st.session_state.active_button == 'payments':
    st.header("📊 Payment Analysis")
    st.markdown("Deep dive into PhonePe payment transactions across India.")

    # 🎯 Objective
    st.subheader("🎯 Objective")
    st.markdown("""
    Analyze payment transaction trends, state-wise distribution, payment mode share, and average transaction value (ATV) to identify growth patterns and user behavior.
    """)

    # Fetch State List
    cursor.execute("SELECT DISTINCT State FROM aggr_trans_data")
    state_list = [row[0] for row in cursor.fetchall()]

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        year_option = st.selectbox("Select Year", ['All', '2018', '2019', '2020', '2021', '2022', '2023'], key='pay_year')

    with col2:
        trans_type_option = st.selectbox("Transaction Type", ['All', 'Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'], key='pay_type')

    with col3:
        state_option = st.selectbox("State", ['All'] + state_list, key='pay_state')

    # Dynamic WHERE Clause
    conditions = []
    if year_option != 'All':
        conditions.append(f"Year='{year_option}'")
    if trans_type_option != 'All':
        conditions.append(f"Transaction_type='{trans_type_option}'")
    if state_option != 'All':
        conditions.append(f"State='{state_option}'")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    # 📊 Key Metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        cursor.execute(f"SELECT SUM(Transaction_amount) FROM aggr_trans_data{where_clause}")
        total_value = cursor.fetchone()[0] or 0
        st.metric("💸 Total Value (₹ Cr)", f"{total_value/1e7:,.2f}")

    with col2:
        cursor.execute(f"SELECT SUM(Transaction_count) FROM aggr_trans_data{where_clause}")
        total_count = cursor.fetchone()[0] or 0
        st.metric("📦 Total Transactions", f"{total_count:,}")

    with col3:
        cursor.execute(f"SELECT AVG(Transaction_amount) FROM aggr_trans_data{where_clause}")
        avg_value = cursor.fetchone()[0] or 0
        st.metric("💰 Avg Value (₹ Cr)", f"{avg_value/1e7:,.2f}")

    col4, col5,col6 = st.columns(3)
    with col4:
        cursor.execute(f"SELECT MAX(Transaction_amount) FROM aggr_trans_data{where_clause}")
        max_value = cursor.fetchone()[0] or 0
        st.metric("🏆 Max Transaction Value (₹ Cr)", f"{max_value/1e7:,.2f}")

    with col5:
        cursor.execute(f"SELECT COUNT(DISTINCT State) FROM aggr_trans_data{where_clause}")
        state_count = cursor.fetchone()[0] or 0
        st.metric("🌏 States Covered", f"{state_count}")

    with col6:
       # Get current year's total payment value
        current_year_query = f"""
        SELECT SUM(Transaction_amount) 
        FROM aggr_trans_data
        {where_clause}
        """
        cursor.execute(current_year_query)
        current_value = cursor.fetchone()[0] or 0
        
        # Get previous year's total payment value
        if 'Year=' in where_clause:
            # Extract year from where_clause
            year_start = where_clause.find("Year='") + 6
            year_end = where_clause.find("'", year_start)
            current_year = where_clause[year_start:year_end]
            prev_year = str(int(current_year) - 1)
            prev_where = where_clause.replace(f"Year='{current_year}'", f"Year='{prev_year}'")
        else:
            # If no year filter, compare latest year vs previous year
            prev_where = " WHERE Year = (SELECT MAX(Year)-1 FROM aggr_trans_data)"
            if where_clause:
                prev_where = where_clause + " AND Year = (SELECT MAX(Year)-1 FROM aggr_trans_data)"
        
        cursor.execute(f"SELECT SUM(Transaction_amount) FROM aggr_trans_data{prev_where}")
        previous_value = cursor.fetchone()[0] or 0
        
        # Calculate YoY growth
        if previous_value > 0:
            yoy_growth = ((current_value - previous_value) / previous_value) * 100
            delta_color = "normal"  # green for positive, red for negative
        else:
            yoy_growth = 0
            delta_color = "off"
        
        st.metric(
            "📈 Payments YoY Growth", 
            f"{yoy_growth:.1f}%",
            delta=f"{yoy_growth:.1f}%" if previous_value > 0 else "N/A",
            delta_color=delta_color
        )
        

    # 📊 Transaction value Trend (Yearly)
    st.subheader("📊 Transaction Value Trend (Yearly)")
    query = f"""
        SELECT Year, Transaction_type, SUM(Transaction_amount) AS Total_amount
        FROM aggr_trans_data
        {where_clause}
        GROUP BY Year, Transaction_type
        ORDER BY Year
    """
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=["Year", "Transaction_amount", "Total_amount"])
    fig = px.line(df, x="Year", y="Total_amount", color="Transaction_amount", markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    
    # 📊 Transaction Count Trend (Yearly)
    st.subheader("📊 Transaction Count Trend (Yearly)")
    query = f"""
        SELECT Year, Transaction_type, SUM(Transaction_count)
        FROM aggr_trans_data
        {where_clause}
        GROUP BY Year, Transaction_type ORDER BY Year
    """
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=["Year", "Transaction_type", "Total_Count"])
    fig = px.line(df, x="Year", y="Total_Count", color="Transaction_type", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # 📊 Average Transaction Value (ATV) by Transaction Type Trend (Yearly)
    st.subheader("📊 Average Transaction Value (ATV) Trend by Transaction Type (Yearly)")

    query = f"""
        SELECT 
            Year, 
            Transaction_type, 
            SUM(Transaction_amount) AS Total_Value, 
            SUM(Transaction_count) AS Total_Volume,
            ROUND(SUM(Transaction_amount)/SUM(Transaction_count), 2) AS ATV
        FROM aggr_trans_data
        {where_clause}
        GROUP BY Year, Transaction_type
        ORDER BY Year, Transaction_type
    """

    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=["Year", "Transaction_type", "Total_Value", "Total_Volume", "ATV"])

    fig = px.line(df, x="Year", y="ATV", color="Transaction_type", markers=True)
    st.plotly_chart(fig, use_container_width=True)


    # 📊 Two Side-by-Side Pie Charts
    st.subheader("📊 Payment Type Distribution")

    query = f"""
        SELECT Transaction_type, SUM(Transaction_amount)
        FROM aggr_trans_data
        {where_clause}
        GROUP BY Transaction_type
    """
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=["Transaction_type", "Transaction_amount"])
    df["% Share"] = df["Transaction_amount"] / df["Transaction_amount"].sum() * 100

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(df, names='Transaction_type', values='Transaction_amount', title="By Transaction Value")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.pie(df, names='Transaction_type', values='% Share', title="By % Share")
        st.plotly_chart(fig2, use_container_width=True)


    # 📊 Top 10 Transaction Types by Total Transaction Amount
    st.subheader("💳 Top 10 Transaction Types by Value")

    query = f"""
        SELECT 
            Transaction_type, 
            SUM(Transaction_amount) AS Total_Amount
        FROM aggr_trans_data
        {where_clause}
        GROUP BY Transaction_type
        ORDER BY Total_Amount DESC
        LIMIT 10
    """

    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=["Transaction_type", "Total_Amount"])
    
    
    def format_amount(val):
        if val >= 1e7:
            return f"{val/1e7:.2f} Cr"
        elif val >= 1e5:
            return f"{val/1e5:.2f} L"
        elif val >= 1e3:
            return f"{val/1e3:.2f} K"
        else:
            return f"{val:.0f}"
        
    # Optional: Format value in Cr, L, K
    df["Total_Amount"] = df["Total_Amount"].apply(lambda x: format_amount(x))

    fig = px.bar(df, x="Transaction_type", y="Total_Amount", text="Total_Amount", color="Transaction_type")
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    
# 📊 Average Transaction Value by State
    st.subheader("💰 Avg Transaction Value by State (Top 10)")
    query = f"""
        SELECT State, AVG(Transaction_amount)
        FROM aggr_trans_data
        {where_clause}
        GROUP BY State ORDER BY AVG(Transaction_amount) DESC LIMIT 10
    """
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=["State", "Avg_Transaction_Value"])
    fig = px.bar(df, x="State", y="Avg_Transaction_Value", text_auto='.2s', color="Avg_Transaction_Value", color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)


# ------------------------- Insurance Section ------------------------- #
elif st.session_state.active_button == 'insurance':
    st.header("🛡️ Insurance Analysis")
    st.markdown("Explore PhonePe's insurance adoption trends across India.")


    st.subheader("🎯 Objective")
    st.markdown("""
    Analyze insurance policy trends, identify top-performing states and districts, and understand geographical distribution to inform strategic decisions.
    """)

    # 📌 Fetch distinct values for filters
    cursor.execute("SELECT DISTINCT State FROM top_insurance_data")
    state_list = sorted([row[0].title() for row in cursor.fetchall()])  # Title case + sort alphabetically

    cursor.execute("SELECT DISTINCT Year FROM top_insurance_data")
    year_list = sorted([row[0] for row in cursor.fetchall()])  # Sorted numerically/alphabetically as appropriate

    cursor.execute("SELECT DISTINCT Quater FROM top_insurance_data")
    quarter_list = sorted([row[0] for row in cursor.fetchall()])  # Sorted numerically/alphabetically as appropriate

    # 📌 Filter widgets
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year = st.selectbox("Select Year", ['All'] + year_list, key='ins_year')

    with col2:
        selected_quarter = st.selectbox("Select Quarter", ['All'] + quarter_list, key='ins_quarter')

    with col3:
        selected_state = st.selectbox("Select State", ['All'] + state_list, key='ins_state')

    # 📌 Construct WHERE clause based on selected filters
    conditions = []

    if selected_year != 'All':
        conditions.append(f"Year = '{selected_year}'")

    if selected_quarter != 'All':
        conditions.append(f"Quater = '{selected_quarter}'")

    if selected_state != 'All':
        conditions.append(f"State = '{selected_state}'")

    # Final WHERE clause string
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    # 📌 Subheader
    st.subheader("Key Insurance Metrics")
    
    # Total Policies Sold
    cursor.execute(f"SELECT SUM(Count) FROM aggr_insurance_data{where_clause}")
    total_policies = cursor.fetchone()[0] or 0

    # Total Premium Collected
    cursor.execute(f"SELECT SUM(Amount) FROM aggr_insurance_data{where_clause}")
    total_premium = cursor.fetchone()[0] or 0

    # Average Premium per Policy
    #avg_premium = total_premium / total_policies if total_policies else 0
    avg_premium = float(total_premium) / float(total_policies) if total_policies else 0

    # Number of States Covered
    cursor.execute(f"SELECT COUNT(DISTINCT State) FROM aggr_insurance_data{where_clause}")
    states_covered = cursor.fetchone()[0] or 0

    # Display Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📄 Total Policies", f"{total_policies:,}")
    with col2:
        st.metric("💰 Total Premium (₹ Cr)", f"{total_premium/1e7:,.2f}")
    with col3:
        st.metric("💵 Avg Premium per Policy (₹)", f"{avg_premium:,.2f}")
    with col4:
        st.metric("🌍 States Covered", f"{states_covered}")
    with col5:
         # Get current year's premium
        current_premium = total_premium
        
        # Get previous year's premium
        prev_where = where_clause.replace(f"Year='{selected_year}'", f"Year='{int(selected_year)-1}'") if selected_year != 'All' else " WHERE Year = (SELECT MAX(Year)-1 FROM aggr_insurance_data)"
        cursor.execute(f"SELECT SUM(Amount) FROM aggr_insurance_data{prev_where}")
        previous_premium = cursor.fetchone()[0] or 0
        
        # Calculate YoY growth percentage
        if previous_premium > 0:
            yoy_growth = ((current_premium - previous_premium) / previous_premium) * 100
            st.metric(
                "📈 Premium YoY Growth",
                f"{yoy_growth:.1f}%",
                delta=f"{yoy_growth:.1f}%",
                delta_color="normal"  # Automatically shows green/red
            )
        else:
            st.metric("📈 Premium YoY Growth", "N/A")


    # 📊 Insurance Trend Over Time
    st.subheader("📈 Insurance Trend Over Time")

    query = f"""
        SELECT Year, SUM(top_insurance_count) AS Total_Policies, SUM(top_insurance_amount) AS Total_Premium
        FROM top_insurance_data
        {where_clause}
        GROUP BY Year
        ORDER BY Year
    """
    cursor.execute(query)
    df_trend = pd.DataFrame(cursor.fetchall(), columns=["Year", "Total_Policies", "Total_Premium"])

    # Convert Decimals to float
    df_trend["Total_Policies"] = df_trend["Total_Policies"].astype(float)
    df_trend["Total_Premium"] = df_trend["Total_Premium"].astype(float)

    fig = px.line(df_trend, x="Year", y=["Total_Policies", "Total_Premium"],
                labels={"value": "Count / Amount", "variable": "Metric"},
                markers=True)
    st.plotly_chart(fig, use_container_width=True)


    # 📊 Top 10 States by Policies Sold
    st.subheader("🏆 Top 10 States by Policies Sold")

    query = f"""
        SELECT State, SUM(top_insurance_count) AS Total_Policies
        FROM top_insurance_data
        {where_clause}
        GROUP BY State
        ORDER BY Total_Policies DESC
        LIMIT 10
    """
    cursor.execute(query)
    df_top_states = pd.DataFrame(cursor.fetchall(), columns=["State", "Total_Policies"])

    fig = px.bar(df_top_states, x="State", y="Total_Policies", text="Total_Policies", color="State")
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # 📊 Top 10 States by Avg Premium Collected
    st.subheader("💸 Top 10 States by Avg Premium Collected")

    query = f"""
        SELECT State, AVG(top_insurance_amount) AS Avg_Premium
        FROM top_insurance_data
        {where_clause}
        GROUP BY State
        ORDER BY Avg_Premium DESC
        LIMIT 10
    """
    cursor.execute(query)
    df_avg_premium = pd.DataFrame(cursor.fetchall(), columns=["State", "Avg_Premium"])

    fig = px.bar(df_avg_premium, x="State", y="Avg_Premium", text="Avg_Premium", color="State")
    fig.update_traces(texttemplate='₹%{text:.2f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # 📊 Top 10 Districts by Policies Sold
    st.subheader("🏙️ Top 10 Districts by Policies Sold")

    query = f"""
        SELECT District, SUM(Top_insurance_count) AS Total_Policies
        FROM top_insurance_data
        {where_clause}
        GROUP BY District
        ORDER BY Total_Policies DESC
        LIMIT 10
    """
    cursor.execute(query)
    df_top_districts = pd.DataFrame(cursor.fetchall(), columns=["District", "Total_Policies"])

    fig = px.bar(df_top_districts, x="District", y="Total_Policies", text="Total_Policies", color="District")
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


# ------------------------- User Section ---------------------- #
elif st.session_state.active_button == 'User':
    st.header("🗺️ User Analysis")
    st.markdown("Explore PhonePe user statistics across India.")
    st.subheader("🎯 Objective")
    st.markdown("""
    Analyze user growth trends, state-wise distribution, and brand performance to identify key insights and opportunities.
    """)

    # 📌 Fetch filters
    cursor.execute("SELECT DISTINCT Year FROM aggr_user_data")
    year_list = sorted([row[0] for row in cursor.fetchall()])

    cursor.execute("SELECT DISTINCT State FROM aggr_user_data")
    state_list = sorted([row[0].title() for row in cursor.fetchall()])

    cursor.execute("SELECT DISTINCT District FROM top_user_data")
    district_list = sorted([row[0] for row in cursor.fetchall()])

# 📌 Filter widgets
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_year = st.selectbox("Select Year", ['All'] + year_list, key='user_year')
    with col2:
        selected_state = st.selectbox("Select State", ['All'] + state_list, key='user_state')
    with col3:
        # District options depend on State selection
        if selected_state != 'All':
            cursor.execute(f"SELECT DISTINCT District FROM top_user_data WHERE State = '{selected_state}'")
            district_options = sorted([row[0] for row in cursor.fetchall()])
            selected_district = st.selectbox("Select District", ['All'] + district_options, key='user_district')
        else:
            selected_district = st.selectbox("Select District", ['All'] + district_list, key='user_district')

    # 📌 WHERE clause builder for aggr_user_data
    aggr_conditions = []
    if selected_year != 'All':
        aggr_conditions.append(f"Year = '{selected_year}'")
    if selected_state != 'All':
        aggr_conditions.append(f"State = '{selected_state}'")
    aggr_where_clause = " WHERE " + " AND ".join(aggr_conditions) if aggr_conditions else ""

    # 📌 WHERE clause builder for top_user_data
    top_conditions = []
    if selected_year != 'All':
        top_conditions.append(f"Year = '{selected_year}'")
    if selected_state != 'All':
        top_conditions.append(f"State = '{selected_state}'")
    if selected_district != 'All':
        top_conditions.append(f"District = '{selected_district}'")
    top_where_clause = " WHERE " + " AND ".join(top_conditions) if top_conditions else ""


    # 📊 KPIs and Top Performers - Single Container
    with st.container():
        st.markdown("## 🚀 User Analysis KPIs")

        # 👉 Total Users
        cursor.execute(f"SELECT SUM(user_count) FROM aggr_user_data {aggr_where_clause}")
        total_users = cursor.fetchone()[0] or 0

        # 👉 Total Brands
        cursor.execute(f"SELECT COUNT(DISTINCT user_brand) FROM aggr_user_data {aggr_where_clause}")
        total_brands = cursor.fetchone()[0] or 0

        # 👉 Total Districts
        cursor.execute(f"SELECT COUNT(DISTINCT District) FROM top_user_data {top_where_clause.replace('aggr_user_data','top_user_data')}")
        total_districts = cursor.fetchone()[0] or 0

        # 👉 Top State
        cursor.execute(f"""
            SELECT State, SUM(user_count) as total FROM aggr_user_data
            {aggr_where_clause} GROUP BY State ORDER BY total DESC LIMIT 1
        """)
        top_state_row = cursor.fetchone()

        # 👉 Top District
        cursor.execute(f"""
            SELECT District, SUM(top_user_count) as total FROM top_user_data
            {top_where_clause.replace('aggr_user_data','top_user_data')}
            GROUP BY District ORDER BY total DESC LIMIT 1
        """)
        top_district_row = cursor.fetchone()

        # 👉 Top Brand
        cursor.execute(f"""
            SELECT user_brand, SUM(user_count) as total FROM aggr_user_data
            {aggr_where_clause} GROUP BY user_brand ORDER BY total DESC LIMIT 1
        """)
        top_brand_row = cursor.fetchone()

        # 📈 Highest Growth Year (ignoring filters)
        cursor.execute("""
            SELECT Year, SUM(user_count) FROM aggr_user_data
            GROUP BY Year ORDER BY SUM(user_count) DESC LIMIT 1
        """)
        top_year_row = cursor.fetchone()

        # 📌 Row 1 KPIs
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1:
            st.metric("👥 Total Users", f"{total_users:,}")
        with kpi_col2:
            st.metric("📱 Total Brands", total_brands)
        with kpi_col3:
            st.metric("📍 Districts Tracked", total_districts)

        # Horizontal separator
        st.markdown("---")

        # 📌 Top Performers Table
        st.markdown("### 🏆 Top Performers")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🏆 Top State**")
            if top_state_row:
                st.markdown(f"<h2 style='text-align:center;color:#22c55e'>{top_state_row[0].title()}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align:center'>{top_state_row[1]:,}</h4>", unsafe_allow_html=True)
            else:
                st.markdown("<h4 style='text-align:center'>N/A</h4>", unsafe_allow_html=True)

        with col2:
            st.markdown("**🏅 Top District**")
            if top_district_row:
                st.markdown(f"<h2 style='text-align:center;color:#22c55e'>{top_district_row[0]}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align:center'>{top_district_row[1]:,}</h4>", unsafe_allow_html=True)
            else:
                st.markdown("<h4 style='text-align:center'>N/A</h4>", unsafe_allow_html=True)

        with col3:
            st.markdown("**📱 Top Brand**")
            if top_brand_row:
                st.markdown(f"<h2 style='text-align:center;color:#22c55e'>{top_brand_row[0]}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align:center'>{top_brand_row[1]:,}</h4>", unsafe_allow_html=True)
            else:
                st.markdown("<h4 style='text-align:center'>N/A</h4>", unsafe_allow_html=True)

        # 📌 Bonus metric below if you want:
        st.markdown("### 📈 Peak Growth Year")
        st.metric("Highest Growth Year", f"{top_year_row[0]} ({top_year_row[1]:,})" if top_year_row else "N/A")
#--------------------------------------------------------------------------------------#


# 📊 Year-wise Distribution (Optional Extra)
    st.subheader("📊 Year-wise User Distribution")
    query = f"""
        SELECT Year, SUM(user_count) AS Total_Users
        FROM aggr_user_data
        {f"WHERE State = '{selected_state}'" if selected_state != 'All' else ""}
        GROUP BY Year ORDER BY Year
    """
    cursor.execute(query)
    df_year_district = pd.DataFrame(cursor.fetchall(), columns=["Year", "Total_Users"])
    fig = px.bar(df_year_district, x="Year", y="Total_Users", title="User Growth Over Years")
    st.plotly_chart(fig, use_container_width=True)

# 📊 state-wise Distribution (Optional Extra)
    st.subheader("📊 State-wise User Distribution")
    query = f"""
        SELECT state, SUM(user_count) AS Total_Users
        FROM aggr_user_data
        {f"WHERE State = '{selected_state}'" if selected_state != 'All' else ""}
        GROUP BY state ORDER BY user_count DESC
    """
    cursor.execute(query)
    df_year_district = pd.DataFrame(cursor.fetchall(), columns=["Year", "Total_Users"])
    fig = px.bar(df_year_district, x="Year", y="Total_Users", title="State User count Over Years")
    st.plotly_chart(fig, use_container_width=True)

#----------------------Brand Performance Over Time---------------------#
    query = f"""
    SELECT Year, user_brand, SUM(user_count) as Users
    FROM aggr_user_data
    GROUP BY Year, user_brand
    """
    cursor.execute(query)
    df_line = pd.DataFrame(cursor.fetchall(), columns=["Year", "Brand", "Users"])

    fig = px.line(df_line, x="Year", y="Users", color="Brand",
                title="Brand Performance Over Years")
    st.plotly_chart(fig, use_container_width=True)

#----------------------User Count by Brand Across States---------------------#
    query = f"""
    SELECT State, user_brand, SUM(user_count) as Users
    FROM aggr_user_data {aggr_where_clause}
    GROUP BY State, user_brand
    """
    cursor.execute(query)
    df_stack = pd.DataFrame(cursor.fetchall(), columns=["State", "Brand", "Users"])

    fig = px.bar(df_stack, x="State", y="Users", color="Brand", barmode="stack",
                title="User Count by Brand Across States")
    st.plotly_chart(fig, use_container_width=True)


#----------------------Market Share Distribution (National)---------------------#
    st.subheader("📊 National Market Share by Brand")
    query = f"""
    SELECT user_brand, SUM(user_count) as Users
    FROM aggr_user_data {aggr_where_clause}
    GROUP BY user_brand
    """
    cursor.execute(query)
    df_pie = pd.DataFrame(cursor.fetchall(), columns=["Brand", "Users"])

    fig = px.pie(df_pie, names="Brand", values="Users", hole=0.4,
                title="National Market Share by Brand")
    st.plotly_chart(fig, use_container_width=True)

#----------------------Top 10 Districts by Top User Count (By State)---------------------#
    st.subheader("🏆 Top 10 Districts by Top User Base")
    query = f"""
    SELECT District, SUM(top_user_count) as TopUsers
    FROM top_user_data {top_where_clause.replace('aggr_user_data','top_user_data')}
    GROUP BY District ORDER BY TopUsers DESC LIMIT 10
    """
    cursor.execute(query)
    df_top_districts = pd.DataFrame(cursor.fetchall(), columns=["District", "TopUsers"])

    fig = px.bar(df_top_districts, x="TopUsers", y="District", orientation="h",
                title="Top 10 Districts by Top User Count")
    st.plotly_chart(fig, use_container_width=True)
    

#----------------------Brand Comparison of Top Users---------------------#
    st.subheader("🏆 Top 10 Brand by User Base")
    #  (from aggr_user_data)
    query = f"""
        SELECT user_brand, SUM(user_count) as Users
        FROM aggr_user_data {aggr_where_clause}
        GROUP BY user_brand
        ORDER BY Users DESC LIMIT 10
    """
    cursor.execute(query)
    df_brand_users = pd.DataFrame(cursor.fetchall(), columns=["Brand", "Users"])

    fig = px.bar(df_brand_users, x="Users", y="Brand", orientation="h",
                title="Brand-wise Total Users")
    st.plotly_chart(fig, use_container_width=True)

#----------------------Top States by User Base---------------------#
    # 📊 Top States by User Base
    st.subheader("🏆 Top 10 States by User Base")
    query = f"""
        SELECT State, SUM(user_count) AS Total_Users
        FROM aggr_user_data
        {f"WHERE Year = '{selected_year}'" if selected_year != 'All' else ""}
        GROUP BY State ORDER BY Total_Users DESC LIMIT 10
    """
    cursor.execute(query)
    df_top_states = pd.DataFrame(cursor.fetchall(), columns=["State", "Total_Users"])
    fig = px.bar(df_top_states, x="Total_Users", y="State", orientation="h", title="Top States by User Base")
    st.plotly_chart(fig, use_container_width=True)


#----------------------District-wise User Count---------------------#
    # 📊 District-wise User Count if a State is selected
    if selected_state != 'All':
        st.subheader(f"📍 Top Districts in {selected_state} by User Count")
        query = f"""
            SELECT District, SUM(top_user_count) AS User_Count
            FROM top_user_data
            WHERE State = '{selected_state}'
            {f"AND Year = '{selected_year}'" if selected_year != 'All' else ""}
            GROUP BY District ORDER BY User_Count DESC LIMIT 10
        """
        cursor.execute(query)
        df_districts = pd.DataFrame(cursor.fetchall(), columns=["District", "User_Count"])
        fig = px.bar(df_districts, x="User_Count", y="District", orientation="h", title=f"Top Districts in {selected_state}")
        st.plotly_chart(fig, use_container_width=True)


# ------------------------- Geographical Section ---------------------- #
elif st.session_state.active_button == 'geo':
    st.header("🗺️ Geographical Analysis")
    st.write("Visualize PhonePe performance geographically across India.")

    # Load GeoJSON for India states
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(geojson_url)
    india_states_geojson = response.json()

    st.subheader("🎯 Objective")
    st.markdown("""
    This page shows geographical penetration of PhonePe Payments, insurance and user distribution across india.
    """)

    # 📌 Fetch Filters
    cursor.execute("SELECT DISTINCT Year FROM map_transaction_data")
    year_list = sorted([row[0] for row in cursor.fetchall()])

    cursor.execute("SELECT DISTINCT State FROM map_transaction_data")
    state_list = sorted([row[0].title() for row in cursor.fetchall()])

    # 📌 Common Filter widgets
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", ['All'] + year_list, key='geo_year')
    with col2:
        selected_state = st.selectbox("Select State", ['All'] + state_list, key='geo_state')

    # 📌 WHERE clause builder
    where_conditions = []
    if selected_year != 'All':
        where_conditions.append(f"Year = '{selected_year}'")
    if selected_state != 'All':
        where_conditions.append(f"State = '{selected_state}'")
    where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""

    # =============================================
    # 📌 COMMON SETUP
    # =============================================
    # Get list of all Indian states from GeoJSON
    all_states = [feature['properties']['ST_NM'] for feature in india_states_geojson['features']]
    
    # Geo settings for all maps (India-only)
    geo_settings = {
        "visible": True,
        "center": {"lat": 20.5937, "lon": 78.9629},  # India's coordinates
        "projection_scale": 5,  # Zoom level
        "showcountries": False,
        "showocean": False,
        "showland": False,
        "subunitcolor": "black",  # State boundary color
        "subunitwidth": 1.5  # Boundary line width
    }

    layout_settings = {
        "geo": {
            "lonaxis_range": [68, 98],  # India's longitudinal bounds
            "lataxis_range": [6, 38]    # India's latitudinal bounds
        },
        "height": 800,
        "margin": {"r":0,"t":40,"l":0,"b":0}
    }

    # =============================================
    # 📌 SECTION 1: PAYMENT TRANSACTIONS
    # =============================================
    st.subheader("💰 Payment Transactions by State")

    # Fetch data
    cursor.execute(f"""
        SELECT State, SUM(Transaction_amount) AS TotalAmount, COUNT(*) AS TransactionCount
        FROM map_transaction_data
        {where_clause}
        GROUP BY State
    """)
    payment_data = cursor.fetchall()

    # Create DataFrame and handle missing states
    df_payments = pd.DataFrame(payment_data, columns=["State", "TotalAmount", "TransactionCount"])
    df_payments['State'] = df_payments['State'].str.title()
    df_payments = df_payments.set_index('State').reindex(all_states, fill_value=0).reset_index()

    # Convert data types
    df_payments = df_payments.astype({
        "TotalAmount": float,
        "TransactionCount": int
    })

    # Create visualization
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        fig_payments = px.choropleth(
            df_payments,
            geojson=india_states_geojson,
            locations="State",
            featureidkey="properties.ST_NM",
            color="TotalAmount",
            color_continuous_scale="blues",
            range_color=(0, df_payments['TotalAmount'].max()),
            hover_data=["TransactionCount"],
            hover_name="State",
            title="<b>Total Payment Amount (₹)</b>",
            height=800  # Only include height here
        )
        
        # Update geographic settings
        fig_payments.update_geos(
            visible=True,
            center={"lat": 20.5937, "lon": 78.9629},
            projection_scale=5,
            showcountries=False,
            showocean=False,
            showland=False,
            subunitcolor="black",
            subunitwidth=1.5
        )
        
        # Update layout settings
        fig_payments.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            geo={
                "lonaxis_range": [68, 98],
                "lataxis_range": [6, 38]
            },
            title_x=0.5
        )
        
        st.plotly_chart(fig_payments, use_container_width=True)

    with col2:
        # Calculate metrics
        active_states = len(df_payments[df_payments['TotalAmount'] > 0])
        total_amount = df_payments['TotalAmount'].sum()
        
        # Display metrics
        st.metric("Total States with Transactions", active_states)
        st.metric("Total Amount", f"₹{total_amount:,.2f}")
        
        # Prepare and display dataframe
        display_df = (df_payments[['State', 'TotalAmount', 'TransactionCount']]
                    .sort_values("TotalAmount", ascending=False)
                    .rename(columns={
                        "TotalAmount": "Amount (₹)",
                        "TransactionCount": "Transactions"
                    }))
        
        st.dataframe(
    display_df,
    height=600,
    hide_index=True,
    column_config={
        "State": st.column_config.Column("State", width="medium"),
        "Amount (₹)": st.column_config.NumberColumn(
            format="%.2f",
            help="Amount in Indian Rupees"
        ),
        "Transactions": st.column_config.NumberColumn(
            format="%d",
            help="Number of transactions"
        )
    }
)

    # =============================================
# 📌 SECTION 2: INSURANCE TRANSACTIONS
# =============================================
    st.subheader("🛡️ Insurance Transactions by State")

    # Fetch data
    cursor.execute(f"""
        SELECT State, SUM(amount) AS TotalAmount, SUM(count) AS PolicyCount
        FROM map_insurance_data
        {where_clause}
        GROUP BY State
    """)
    insurance_data = cursor.fetchall()

    # Create DataFrame and handle missing states
    df_insurance = pd.DataFrame(insurance_data, columns=["State", "TotalAmount", "PolicyCount"])
    df_insurance['State'] = df_insurance['State'].str.title()
    df_insurance = df_insurance.set_index('State').reindex(all_states, fill_value=0).reset_index()

    # Add ranking and convert data types
    df_insurance['Rank'] = df_insurance['TotalAmount'].rank(ascending=False, method='min').astype(int)
    df_insurance = df_insurance.astype({
        "TotalAmount": float,
        "PolicyCount": int
    })

    # Create visualization
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        fig_insurance = px.choropleth(
            df_insurance,
            geojson=india_states_geojson,
            locations="State",
            featureidkey="properties.ST_NM",
            color="TotalAmount",
            color_continuous_scale="greens",
            range_color=(0, df_insurance['TotalAmount'].max()),
            hover_data=["PolicyCount"],
            hover_name="State",
            title="<b>Total Insurance Amount (₹)</b>",
            height=800
        )
        
        fig_insurance.update_geos(
            visible=True,
            center={"lat": 20.5937, "lon": 78.9629},
            projection_scale=5,
            showcountries=False,
            showocean=False,
            showland=False,
            subunitcolor="black",
            subunitwidth=1.5
        )
        
        fig_insurance.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            geo={
                "lonaxis_range": [68, 98],
                "lataxis_range": [6, 38]
            },
            title_x=0.5
        )
        
        st.plotly_chart(fig_insurance, use_container_width=True)

    with col2:
        active_states = len(df_insurance[df_insurance['TotalAmount'] > 0])
        total_policies = df_insurance['PolicyCount'].sum()
        
        st.metric("Active States", active_states)
        st.metric("Total Policies", f"{total_policies:,}")
        
        display_df = (df_insurance[['Rank', 'State', 'TotalAmount', 'PolicyCount']]
                    .sort_values("Rank")
                    .rename(columns={
                        "TotalAmount": "Amount (₹)",
                        "PolicyCount": "Policies"
                    }))
        
        st.dataframe(
    display_df,
    height=600,
    hide_index=True,
    column_config={
        "Rank": st.column_config.NumberColumn(width="small"),
        "State": st.column_config.Column(width="medium"),
        "Amount (₹)": st.column_config.NumberColumn(
            format="%.2f",
            help="Insurance amount in Rupees"
        ),
        "Policies": st.column_config.NumberColumn(
            format="%d",
            help="Number of policies"
        )
    }
)

    # =============================================
# 📌 SECTION 3: USER DISTRIBUTION
# =============================================
    st.subheader("👥 User Distribution by State")

    # Fetch data
    cursor.execute(f"""
        SELECT State, SUM(Registered_users) AS TotalUsers, COUNT(DISTINCT District) AS DistrictsCovered
        FROM map_user_data
        {where_clause}
        GROUP BY State
    """)
    user_data = cursor.fetchall()

    # Create DataFrame and handle missing states
    df_users = pd.DataFrame(user_data, columns=["State", "TotalUsers", "DistrictsCovered"])
    df_users['State'] = df_users['State'].str.title()
    df_users = df_users.set_index('State').reindex(all_states, fill_value=0).reset_index()

    # Convert data types
    df_users = df_users.astype({
        "TotalUsers": int,
        "DistrictsCovered": int
    })

    # Create visualization
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        fig_users = px.choropleth(
            df_users,
            geojson=india_states_geojson,
            locations="State",
            featureidkey="properties.ST_NM",
            color="TotalUsers",
            color_continuous_scale="reds",
            range_color=(0, df_users['TotalUsers'].max()),
            hover_data=["DistrictsCovered"],
            hover_name="State",
            title="<b>Total Registered Users</b>",
            height=800
        )
        
        fig_users.update_geos(
            visible=True,
            center={"lat": 20.5937, "lon": 78.9629},
            projection_scale=5,
            showcountries=False,
            showocean=False,
            showland=False,
            subunitcolor="black",
            subunitwidth=1.5
        )
        
        fig_users.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            geo={
                "lonaxis_range": [68, 98],
                "lataxis_range": [6, 38]
            },
            title_x=0.5
        )
        
        st.plotly_chart(fig_users, use_container_width=True)

    with col2:
        active_states = len(df_users[df_users['TotalUsers'] > 0])
        total_users = df_users['TotalUsers'].sum()
        
        st.metric("Active States", active_states)
        st.metric("Total Users", f"{total_users:,}")
        
        display_df = (df_users[['State', 'TotalUsers', 'DistrictsCovered']]
                    .sort_values("TotalUsers", ascending=False)
                    .rename(columns={
                        "TotalUsers": "Users",
                        "DistrictsCovered": "Districts"
                    }))
        
        st.dataframe(
        display_df,
        height=600,
        hide_index=True,
        column_config={
            "State": st.column_config.Column(width="medium"),
            "Users": st.column_config.NumberColumn(
                format="%d",
                help="Number of registered users"
            ),
            "Districts": st.column_config.NumberColumn(
                format="%d",
                help="Districts covered"
            )
        }
    )


st.info("Use the Payments, Insurance, User, and Geographical buttons at the top to explore detailed insights 📊📱")


