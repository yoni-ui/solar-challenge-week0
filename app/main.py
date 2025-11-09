import streamlit as st
import pandas as pd
import sys
import os

# Add the app directory to the path so utils can be imported
sys.path.append(os.path.dirname(__file__))

# Import utility functions
try:
    from utils import load_and_preprocess_data, create_country_comparison_plot, create_time_series_plot, create_top_regions_table, COUNTRIES
except ImportError as e:
    st.error(f"Error loading utility functions: {e}. Ensure utils.py is in the app directory.")
    st.stop()


def main():
    """Main function to run the Streamlit dashboard."""
    
    st.set_page_config(
        page_title="Solar Farm Investment Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("☀️ West Africa Solar Farm Feasibility Dashboard")
    st.markdown("---")

    # --- Data Loading ---
    with st.spinner("Loading and processing solar data..."):
        df_combined = load_and_preprocess_data()

    # --- Sidebar for Filtering ---
    st.sidebar.header("Filter & Settings")
    
    selected_countries = st.sidebar.multiselect(
        'Select Countries for Comparison',
        options=COUNTRIES,
        default=COUNTRIES,
    )

    granularity = st.sidebar.radio(
        'Select Time Series Granularity',
        options=['Daily', 'Weekly', 'Monthly'],
        index=0
    )

    # Filter the DataFrame based on selections
    df_filtered = df_combined[df_combined['Country'].isin(selected_countries)]


    # --- Dashboard Layout ---
    
    # 1. Key Performance Indicators (KPIs) and Top Regions Table
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("1. Cross-Country GHI Distribution")
        st.markdown("Compare the variability and central tendency (median) of Global Horizontal Irradiance (GHI) across selected regions.")
        
        if df_filtered.empty:
            st.warning("Please select at least one country.")
        else:
            comparison_chart = create_country_comparison_plot(df_filtered)
            st.altair_chart(comparison_chart, use_container_width=True)

    with col2:
        st.header("Top Regions (By Mean GHI)")
        # Display the aggregated table for all loaded countries
        top_regions_table = create_top_regions_table(df_combined)
        st.dataframe(top_regions_table, use_container_width=True, hide_index=True)
        st.markdown(
            """
            *Data Source: Cleaned, Pre-processed CSVs.*
            """
        )

    st.markdown("---")

    # 2. Time Series Analysis
    st.header(f"2. GHI Time Series Analysis ({granularity} Mean)")
    st.markdown("View average GHI trends over the full period to identify seasonal patterns for each country.")

    if df_filtered.empty:
        st.warning("Cannot display Time Series without data.")
    else:
        time_series_chart = create_time_series_plot(df_filtered, granularity)
        st.altair_chart(time_series_chart, use_container_width=True)


    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
            border: none;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()