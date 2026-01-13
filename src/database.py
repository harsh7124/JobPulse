import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# 1. Setup the Database Connection
# We use SQLAlchemy for "Production" grade ORM (Object Relational Mapping)
DB_PATH = 'sqlite:///data/jobs.db'
engine = create_engine(DB_PATH, echo=False)

def load_data_to_db(df, table_name="job_postings"):
    """
    Takes a Pandas DataFrame and saves it to the SQL database.
    if_exists='append': Adds new jobs without deleting old ones.
    """
    try:
        with engine.connect() as conn:
            df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"✅ Success: Loaded {len(df)} rows into {table_name}")
    except Exception as e:
        print(f"❌ Error loading data: {e}")

def fetch_data_from_db(query="SELECT * FROM job_postings"):
    """
    Reads data from SQL back into a DataFrame for the dashboard.
    """
    try:
        return pd.read_sql(query, engine)
    except Exception:
        return pd.DataFrame() # Return empty if DB doesn't exist yet