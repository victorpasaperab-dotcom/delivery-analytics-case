# Delivery Performance Analytics Dashboard

## Project Overview
This project provides a comprehensive analysis of delivery operations, focusing on 
**Actual Time of Delivery (ATD), spatial distribution, and temporal trends. 
It includes an interactive Streamlit dashboard for stakeholder insights.

## Key Features
- **ATD Segmentation**: Orders are categorized into five performance buckets (0-10 min, 11-20 min, etc.).
- **Interactive Filtering**: Dual-filter logic allowing users to slice data by Date Range and Territory.
- **Dual-Axis Monitoring**: Tracks Order Volume vs. Avg ATD over time to identify operational bottlenecks.

## Tech Stack
- **Python 3.x**: Data processing and visualization.
- **Streamlit**: Dashboard framework.
- **Plotly**: Interactive charting.

Repository Structure
app.py: Main entry point for the dashboard.
modules/: Contains modularized logic for data loading and visualization.
sql/: Includes the T-SQL script for dynamic weekly data extraction.
data/: Directory for the source CSV dataset.
requirements.txt: Project dependencies.

## Installation & Setup

Follow these steps to run the dashboard locally:

**Clone the repository**:

      git clone <https://github.com/victorpasaperab-dotcom/delivery-analytics-case>
   
      cd delivery_analytics_case
   
**Create enviroment and install requirements**

      python -m venv venv

      .\venv\Scripts\activate
   
      pip install -r requirements.txt
   
      mkdir data
   
**Paste csv file on data folder**

      streamlit run app2.py
