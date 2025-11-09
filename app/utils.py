import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime

# Define the relative path where cleaned data is expected
DATA_DIR = '../data/' 
COUNTRIES = ['Benin', 'Sierra_Leone', 'Togo']

@st.cache_data
def load_and_preprocess_data():
    """
    Loads all cleaned country data, combines them, and performs necessary
    time-based preprocessing.
    NOTE: This assumes the cleaned CSVs are available in the DATA_DIR.
    If the files are not found, it generates structured mock data for demonstration.
    """
    all_data = []
    
    try:
        for country in COUNTRIES:
            file_path = f'{DATA_DIR}{country.lower()}_clean.csv'
            df = pd.read_csv(file_path)
            
            # Ensure proper datetime format
            df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
            df.set_index('TIMESTAMP', inplace=True)
            
            # Ensure GHI is present and handle potential missingness after cleaning
            if 'GHI' not in df.columns:
                 raise ValueError(f"GHI column missing in {file_path}")
            
            df['Country'] = country
            all_data.append(df[['GHI', 'Country']])

    except FileNotFoundError:
        # Fallback: Generate mock data if cleaned CSVs are not found (for demonstration/testing)
        st.warning("Cleaned CSV files not found. Generating mock data for visualization.")
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2023, 1, 1)
        
        for country in COUNTRIES:
            dates = pd.date_range(start=start_date, end=end_date, freq='H', inclusive='left')
            # Mock GHI based on country (e.g., lower std dev for 'Togo' to show variance)
            if country == 'Benin':
                ghi = np.random.normal(loc=300, scale=350, size=len(dates))
            elif country == 'Sierra_Leone':
                ghi = np.random.normal(loc=350, scale=300, size=len(dates))
            else: # Togo
                ghi = np.random.normal(loc=250, scale=400, size=len(dates))

            # Ensure GHI is non-negative
            ghi[ghi < 0] = 0
            
            df = pd.DataFrame({'GHI': ghi}, index=dates)
            df.index.name = 'TIMESTAMP'
            df['Country'] = country
            all_data.append(df)

    # Combine all data into one DataFrame
    combined_df = pd.concat(all_data)
    return combined_df

def create_country_comparison_plot(df):
    """Generates an interactive Box Plot comparing GHI across countries using Altair."""
    # Import inside function to avoid circular dependency in some environments
    import altair as alt

    chart = alt.Chart(df).mark_boxplot(extent='min-max', size=30).encode(
        x=alt.X('Country:N', axis=alt.Axis(title='Country')),
        y=alt.Y('GHI:Q', axis=alt.Axis(title='Global Horizontal Irradiance (W/m²)')),
        color='Country:N',
        tooltip=['Country', 'median(GHI)', 'min(GHI)', 'max(GHI)']
    ).properties(
        title='Cross-Country Comparison of GHI Distribution'
    ).interactive()
    
    return chart

def create_time_series_plot(df, granularity):
    """Generates a time-series line chart for GHI, aggregated by granularity."""
    import altair as alt

    # Resample GHI data based on selected granularity (e.g., 'D' for Daily Mean)
    if granularity == 'Daily':
        resampled_df = df.groupby('Country')['GHI'].resample('D').mean().reset_index()
    elif granularity == 'Weekly':
        resampled_df = df.groupby('Country')['GHI'].resample('W').mean().reset_index()
    else: # Monthly
        resampled_df = df.groupby('Country')['GHI'].resample('M').mean().reset_index()
    
    chart = alt.Chart(resampled_df).mark_line(point=True).encode(
        x=alt.X('TIMESTAMP:T', axis=alt.Axis(title=f'{granularity} Period')),
        y=alt.Y('GHI:Q', axis=alt.Axis(title='Average GHI (W/m²)')),
        color='Country:N',
        tooltip=['TIMESTAMP', 'Country', alt.Tooltip('GHI', format='.2f')]
    ).properties(
        title=f'Average GHI Over Time (Aggregated by {granularity})'
    ).interactive()
    
    return chart

def create_top_regions_table(df):
    """Generates a table showing the mean GHI for each country."""
    # Calculate mean GHI per country and reset index to make 'Country' a column
    mean_ghi = df.groupby('Country')['GHI'].mean().reset_index()
    
    # Rename columns for clarity and sort by GHI
    mean_ghi.columns = ['Country', 'Average GHI (W/m²)']
    mean_ghi['Average GHI (W/m²)'] = mean_ghi['Average GHI (W/m²)'].round(2)
    mean_ghi = mean_ghi.sort_values(by='Average GHI (W/m²)', ascending=False)
    
    return mean_ghi