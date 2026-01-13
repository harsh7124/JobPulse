import requests
import pandas as pd
from datetime import datetime
import os
from src.database import load_data_to_db
from faker import Faker # Fallback if API fails

# CONFIGURATION
ADZUNA_APP_ID = "b988d600" # We read these from Environment Variables for security
ADZUNA_APP_KEY = "b98a39cf183206f4402fcf9c69588940"
BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"

def fetch_real_jobs():
    """Fetches real jobs from Adzuna API"""
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        print("⚠️ No API Keys found. Switching to Mock Data Mode.")
        return generate_mock_jobs()

    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'results_per_page': 50,
        'what': 'software engineer', # Search term
        'content-type': 'application/json'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Parse the JSON response into our format
        jobs = []
        for item in data.get('results', []):
            jobs.append({
                'title': item.get('title'),
                'company': item.get('company', {}).get('display_name'),
                'location': item.get('location', {}).get('display_name'),
                'salary': item.get('salary_min', 0), # Simplified
                'posted_at': item.get('created'),
                'source': 'Adzuna API'
            })
        
        return pd.DataFrame(jobs)
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return pd.DataFrame()

def generate_mock_jobs(n=20):
    """Fallback generator so the app never breaks"""
    fake = Faker()
    data = []
    for _ in range(n):
        data.append({
            'title': fake.job(),
            'company': fake.company(),
            'location': fake.city(),
            'salary': fake.random_int(60000, 150000),
            'posted_at': datetime.now(),
            'source': 'Synthetic'
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("🚀 Starting Data Ingestion...")
    df = fetch_real_jobs()
    if not df.empty:
        # Data Cleaning: Ensure no duplicates before loading
        df['ingested_at'] = datetime.now()
        load_data_to_db(df)
        print("🎉 Data Pipeline Completed Successfully.")
    else:
        print("⚠️ No data fetched.")