import pandas as pd
from datetime import datetime, timedelta
import re

# Function to clean strings
def clean_strings(column_values):
    cleaned_values = column_values.apply(lambda x: re.sub(r'^\W+|[\[\]\(\)]|,+', '', str(x).strip()))
    return cleaned_values

# Function to fetch data for the last 15 days
def fetch_data():
    for i in range(15):
        date_to_check = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        url = f"https://assets.publishing.service.gov.uk/media/66434d1fae748c43d3793aa0/{date_to_check}_-_Worker_and_Temporary_Worker.csv"
        try:
            df = pd.read_csv(url)
            for column in df.columns:
                df[column] = clean_strings(df[column])
            df['Town/City'] = df['Town/City'].apply(lambda x: x.title())
            return df, date_to_check
        except Exception as e:
            continue
    return None, None
