import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import re



# Page configuration
st.set_page_config(
    page_title="UK Work Visa Dashboard",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


# Function to clean the beginning of strings for any symbols, remove brackets, commas, and extra spaces
def clean_strings(column_values):
    cleaned_values = column_values.apply(lambda x: re.sub(r'^\W+|[\[\]\(\)]|,+', '', str(x).strip()))
    return cleaned_values

# Setting initial staus false
status_found = False

# Iterate over the past 15 days
for i in range(15):
    # Get the date to check by subtracting days from the current date
    date_to_check = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
    
    # Construct the URL
    url = f"https://assets.publishing.service.gov.uk/media/66434d1fae748c43d3793aa0/{date_to_check}_-_Worker_and_Temporary_Worker.csv"
    
    try:
        # Read the CSV file from the URL
        df = pd.read_csv(url)
        
        # Print the status found and break the loop
        print(f"Found for {date_to_check}")

        for column in df.columns:
            df[column] = clean_strings(df[column])
        
        #Standardising town/city (making all names in title case)
        df['Town/City'] = df['Town/City'].apply(lambda x: x.title())

        status_found = True
        break  
    
    except Exception as e:
        # Print error message if reading the CSV file fails
        print(f"Didn't find CSV for {date_to_check}: {e}")

# Print a message if status is not found for the past 15 days
if not status_found:
    print("Can't find list for the past 15 days.")

# Title and sidebar for the app
st.title("UK Work Visa Routes Explorer")
st.write(f"last updated: {(datetime.now() - timedelta(days=i)).strftime('%d-%m-%Y')}")


# Search bar for organisation
st.sidebar.header('Search Organisation')
search_term = st.sidebar.text_input('Enter organisation name to search')

# Apply filters
filtered_data = df.copy()

if search_term:
    st.header('Search Results')
    filtered_data = filtered_data[filtered_data['Organisation Name'].str.contains(search_term, case=False, na=False)]

# Sidebar filters
st.sidebar.header('Filter Options')
selected_city = st.sidebar.multiselect('Select Town/City', df['Town/City'].unique())
selected_type = st.sidebar.multiselect('Select Type', df['Type & Rating'].unique())
selected_visa_route = st.sidebar.multiselect('Select Visa Route', df['Route'].unique())


if selected_city:
    filtered_data = filtered_data[filtered_data['Town/City'].isin(selected_city)]
if selected_type:
    filtered_data = filtered_data[filtered_data['Type & Rating'].isin(selected_type)]
if selected_visa_route:
    filtered_data = filtered_data[filtered_data['Route'].isin(selected_visa_route)]


# Overview Section
st.header('Overview')

col1, col2 = st.columns(2)
with col1:
    st.subheader('Total Number of Organisations')
    st.write(filtered_data['Organisation Name'].nunique())
with col2:
    st.subheader('Total Number of Visa Routes')
    st.write(filtered_data['Route'].nunique())

col1, col2 = st.columns([1,2])
with col1:
    st.subheader('Top Cities/Towns')
    st.write(filtered_data['Town/City'].value_counts().head(5))
with col2:
    st.subheader('Top Visa Routes')
    st.write(filtered_data['Route'].value_counts())


# Show filtered data
st.header('Data')
st.dataframe(filtered_data,hide_index=True, column_order=('Organisation Name','Town/City','Route','Type & Rating'))


# Bar chart for Organisation count by Town/City
st.subheader('Organisation Count by Town/City')
city_count = filtered_data['Town/City'].value_counts()
st.bar_chart(city_count)

# Bar chart for Organisation count by Visa Route
st.subheader('Organisation Count by Visa Route')
visa_route_count = filtered_data['Route'].value_counts()
st.bar_chart(visa_route_count)

