import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import re
from data_utils import clean_strings, fetch_data

# Set page configuration
st.set_page_config(
    page_title="UK Work Visa Dashboard",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable dark theme for Altair plots
import altair as alt
alt.themes.enable("dark")

def main():
    # Fetch data
    df, last_updated_date = fetch_data()

    # Display message if data not found
    if df is None:
        st.error("Data not available for the past 15 days.")
        return

    # Title and last updated date
    st.title("UK Work Visa Routes Explorer")
    st.write(f"Last updated: {last_updated_date}")

    # Sidebar for search and filters
    st.sidebar.header('Search Organisation')
    search_term = st.sidebar.text_input('Enter organisation name to search')

    # Apply search filter
    filtered_data = df.copy()
    if search_term:
        st.header('Search Results')
        filtered_data = filtered_data[filtered_data['Organisation Name'].str.contains(search_term, case=False, na=False)]

    # Sidebar filters
    st.sidebar.header('Filter Options')
    selected_city = st.sidebar.multiselect('Select Town/City', df['Town/City'].unique())
    selected_type = st.sidebar.multiselect('Select Type', df['Type & Rating'].unique())
    selected_visa_route = st.sidebar.multiselect('Select Visa Route', df['Route'].unique())

    # Apply filters
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
    st.dataframe(filtered_data, hide_index=True, column_order=('Organisation Name','Town/City','Route','Type & Rating'))

    # Bar chart for Organisation count by Town/City
    st.subheader('Organisation Count by Town/City')
    city_count = filtered_data['Town/City'].value_counts()
    st.bar_chart(city_count)

    # Bar chart for Organisation count by Visa Route
    st.subheader('Organisation Count by Visa Route')
    visa_route_count = filtered_data['Route'].value_counts()
    st.bar_chart(visa_route_count)

if __name__ == "__main__":
    main()
