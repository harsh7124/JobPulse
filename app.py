import streamlit as st
import plotly.express as px
from src.database import fetch_data_from_db

st.set_page_config(page_title="JobPulse Pro", layout="wide")

# 1. READ DATA (No calculation here, just reading)
df = fetch_data_from_db()

# 2. HANDLE EMPTY STATE (If script hasn't run yet)
if df.empty:
    st.warning("No data found in database. Please run 'src/ingestion.py' first.")
    st.stop()

# --- NEW FEATURE: Sidebar Search ---
st.sidebar.header("🔎 Filter Jobs")
search_query = st.sidebar.text_input("Search Job Titles (e.g., Data, Manager)")

# Filter the dataframe based on search
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_query, case=False, na=False)]

# 3. DASHBOARD
st.title("🌍 Global Job Market Pulse")
st.markdown(f"**Data Sources:** {filtered_df['source'].unique()}")

# Top Metrics (Updated to use 'filtered_df' so numbers change when you search)
c1, c2, c3 = st.columns(3)
c1.metric("Total Jobs Tracked", len(filtered_df))
if not filtered_df.empty:
    c2.metric("Avg Salary Estimate", f"${filtered_df['salary'].mean():,.0f}")
    c3.metric("Latest Ingestion", str(filtered_df['ingested_at'].max())[:16])
else:
    c2.metric("Avg Salary", "$0")
    c3.metric("Latest Ingestion", "N/A")

st.divider()

# 4. VISUALIZATION
col1, col2 = st.columns(2)

with col1:
    # Existing Chart: Top Roles
    if not filtered_df.empty:
        top_roles = filtered_df['title'].value_counts().head(10).reset_index()
        top_roles.columns = ['Job Title', 'Count']
        fig = px.bar(top_roles, x='Job Title', y='Count', title="🔥 Top 10 Hot Roles", color='Count')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # --- NEW FEATURE: Top Locations ---
    if 'location' in filtered_df.columns and not filtered_df.empty:
        top_locs = filtered_df['location'].value_counts().head(10).reset_index()
        top_locs.columns = ['Location', 'Count']
        fig2 = px.bar(top_locs, x='Location', y='Count', title="📍 Top Locations", color='Count')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Location data not available or no jobs found.")
