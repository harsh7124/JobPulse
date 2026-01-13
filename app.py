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

# 3. DASHBOARD
st.title("🌍 Global Job Market Pulse")
st.markdown(f"**Data Sources:** {df['source'].unique()}")

# Top Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Total Jobs Tracked", len(df))
c2.metric("Avg Salary Estimate", f"${df['salary'].mean():,.0f}")
c3.metric("Latest Ingestion", str(df['ingested_at'].max())[:16])

# Visualization
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(df['title'].value_counts().head(10), title="Top 10 Hot Roles")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.histogram(df, x="salary", nbins=20, title="Salary Distribution Curve")
    st.plotly_chart(fig2, use_container_width=True)