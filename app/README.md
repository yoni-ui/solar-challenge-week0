Interactive Solar Data Dashboard (Bonus Task)

This folder contains the Streamlit application for visualizing the cleaned solar farm data from the three West African countries (Benin, Sierra Leone, and Togo), supporting the final investment recommendation.

The dashboard allows users to compare Global Horizontal Irradiance (GHI) distributions and analyze seasonal trends dynamically.

📁 File Structure

.
└── app/
    ├── main.py   # Main Streamlit application
    ├── utils.py  # Data loading, processing, and Altair chart functions
    └── README.md # This file


🚀 Usage and Deployment

1. Prerequisites

Before running or deploying, ensure you have the following packages installed:

pip install streamlit pandas numpy altair


(Note: If you are running the app locally with actual data, your cleaned CSV files must be present in a directory named data/ one level above the app/ directory).

2. Local Execution

To run the application locally from the root of your repository:

streamlit run app/main.py


3. Key Features

The dashboard includes the following interactive elements and visualizations:

Feature

Type

Description

Country Selector

Multiselect Widget

Allows the user to select one or more countries for comparison charts.

Time Granularity

Radio Button Widget

Switches the Time Series chart aggregation (Daily, Weekly, or Monthly mean GHI).

GHI Box Plot

Altair Chart

Compares the distribution, median, and range of GHI values across selected countries.

GHI Time Series

Altair Chart

Visualizes the trend of average GHI over time for seasonal analysis.

Top Regions Table

Dataframe

Ranks all countries by their overall mean GHI.