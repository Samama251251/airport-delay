"""
US Flight Analytics Dashboard - Streamlit Version
Interactive dashboard with three visualizations:
1. US State Choropleth Map
2. Animated Airline Bar Chart Race
3. Hierarchical Sunburst Chart
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# Import chart functions
from components.charts import (
    create_choropleth,
    create_animated_airline_chart,
    create_sunburst,
    COLORS
)

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="US Flight Analytics Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for light theme styling
st.markdown("""
    <style>
    /* Force light theme */
    .main {
        background-color: #f8fafc;
    }
    
    /* Streamlit default elements light theme */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdfa 100%);
        border-bottom: 3px solid #0d9488;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-radius: 0.75rem;
    }
    
    .header-title {
        color: #134e4a;
        font-size: 2.25rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    .header-subtitle {
        color: #0d9488;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    /* Sidebar styling - light theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0fdfa 100%);
        border-right: 2px solid #99f6e4;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #ffffff 0%, #f0fdfa 100%);
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] .css-10trblm {
        color: #134e4a;
    }
    
    /* Section headers */
    h1, h2, h3 {
        color: #134e4a !important;
        font-weight: 700;
    }
    
    /* Regular text */
    p, span, div {
        color: #1e293b;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #0d9488;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #134e4a;
        font-weight: 600;
    }
    
    [data-testid="stMetricDelta"] {
        color: #0f766e;
    }
    
    /* Selectbox and input styling */
    .stSelectbox label, .stMultiSelect label {
        color: #134e4a !important;
        font-weight: 600;
    }
    
    /* Dropdown select boxes - force light mode */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    .stMultiSelect > div > div {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Dropdown menu items */
    [data-baseweb="select"] > div,
    [data-baseweb="popover"] > div {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Selected option text */
    [data-baseweb="select"] span {
        color: #1e293b !important;
    }
    
    /* Dropdown arrow icon */
    [data-baseweb="select"] svg {
        fill: #134e4a !important;
    }
    
    /* Dropdown options list */
    [role="listbox"] {
        background-color: #ffffff !important;
    }
    
    [role="option"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    [role="option"]:hover {
        background-color: #f0fdfa !important;
        color: #0d9488 !important;
    }
    
    /* Multi-select tags */
    [data-baseweb="tag"] {
        background-color: #ccfbf1 !important;
        color: #134e4a !important;
    }
    
    /* Input fields */
    input, textarea {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #f0fdfa;
        border-left: 4px solid #0d9488;
        color: #134e4a;
    }
    
    /* Divider */
    hr {
        border-color: #99f6e4;
    }
    
    /* Remove default dark theme elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Charts container background */
    .js-plotly-plot {
        background-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING
# ============================================

@st.cache_data
def load_data():
    """Load all required data files"""
    data_dir = Path(__file__).parent / "data" / "aggregated"
    
    return {
        'state_metrics': pd.read_csv(data_dir / "state_metrics.csv"),
        'daily_airline_metrics': pd.read_csv(data_dir / "daily_airline_metrics.csv"),
        'hierarchy_data': pd.read_csv(data_dir / "hierarchy_data.csv"),
        'airline_metrics': pd.read_csv(data_dir / "airline_metrics.csv"),
        'summary_stats': pd.read_csv(data_dir / "summary_stats.csv")
    }

# Load data
try:
    data = load_data()
    state_metrics = data['state_metrics']
    daily_airline_metrics = data['daily_airline_metrics']
    hierarchy_data = data['hierarchy_data']
    airline_metrics = data['airline_metrics']
    summary_stats = data['summary_stats']
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ============================================
# HEADER
# ============================================

st.markdown("""
    <div class="header-container">
        <h1 class="header-title">✈️ US Flight Analytics Dashboard</h1>
        <p class="header-subtitle">Interactive analysis of flight data • January 2018</p>
    </div>
""", unsafe_allow_html=True)

# ============================================
# KPI CARDS
# ============================================

st.markdown("### 📊 Key Performance Indicators")

# Get summary statistics
stats = summary_stats.to_dict('records')[0]
avg_delay = stats.get('AvgDepartureDelay', 0)
cancel_rate = stats.get('CancellationRate', 0)
total_cancelled = int(stats.get('TotalCancelled', 0))
total_flights = int(stats.get('TotalFlights', 0))

# Create KPI columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Average Departure Delay",
        value=f"{avg_delay:.1f} min",
        delta=None,
        help="Average delay across all flights in minutes"
    )

with col2:
    st.metric(
        label="Cancellation Rate",
        value=f"{cancel_rate:.2f}%",
        delta=f"{total_cancelled:,} cancelled",
        help="Percentage of flights cancelled"
    )

with col3:
    st.metric(
        label="Total Flights",
        value=f"{total_flights:,}",
        delta=None,
        help="Total number of flights in January 2018"
    )

with col4:
    on_time_rate = 100 - cancel_rate - (avg_delay / 100 * 10)  # Approximate
    st.metric(
        label="Operational Flights",
        value=f"{total_flights - total_cancelled:,}",
        delta=None,
        help="Flights that actually operated"
    )

st.markdown("---")

# ============================================
# SIDEBAR INFO
# ============================================

st.sidebar.header("ℹ️ About")
st.sidebar.info("""
**US Flight Analytics Dashboard**

Interactive flight analytics for January 2018 featuring:
- 🗺️ US state-level metrics
- 📊 Daily airline performance animation
- 🌅 Multi-level hierarchy drill-down

**Data Source**: US Flight Data 2018

Each visualization has its own filters and controls located directly above the chart.
""")

# ============================================
# VISUALIZATION 1: US STATE CHOROPLETH MAP
# ============================================

st.markdown("## 🗺️ US Flight Metrics by State")

# Map controls - positioned above the map
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    map_metric = st.selectbox(
        "Map Metric",
        options=['AvgDepDelay', 'CancellationRate', 'FlightCount'],
        format_func=lambda x: {
            'AvgDepDelay': 'Average Delay',
            'CancellationRate': 'Cancellation Rate',
            'FlightCount': 'Flight Volume'
        }[x],
        key="map_metric",
        help="Select which metric to display on the map"
    )

st.markdown(f"""
    <p class="section-subtitle">
        Interactive map showing {
            'average departure delay' if map_metric == 'AvgDepDelay' 
            else 'cancellation rate' if map_metric == 'CancellationRate'
            else 'total flight volume'
        } across all US states
    </p>
""", unsafe_allow_html=True)

# Create and display choropleth
try:
    fig_map = create_choropleth(state_metrics, metric=map_metric)
    st.plotly_chart(fig_map, use_container_width=True, key="choropleth")
except Exception as e:
    st.error(f"Error creating map: {e}")

st.markdown("---")

# ============================================
# VISUALIZATION 2: ANIMATED AIRLINE CHART
# ============================================

st.markdown("## 📊 Daily Airline Performance Animation")

# Animation controls - positioned above the chart
col1, col2 = st.columns(2)

with col1:
    # Get unique airlines for multiselect
    all_airlines = sorted(daily_airline_metrics['Airline'].unique().tolist())
    selected_airlines = st.multiselect(
        "Select Airlines",
        options=all_airlines,
        default=[],
        key="selected_airlines",
        help="Select specific airlines to display (leave empty to show all)"
    )

with col2:
    animation_metric = st.selectbox(
        "Select Metric",
        options=['FlightCount', 'AvgDepDelay', 'OnTimeRate', 'CancellationRate'],
        format_func=lambda x: {
            'FlightCount': 'Flight Count',
            'AvgDepDelay': 'Avg Delay (min)',
            'OnTimeRate': 'On-Time %',
            'CancellationRate': 'Cancellation %'
        }[x],
        key="animation_metric",
        help="Select which metric to animate over time"
    )

st.markdown("""
    <p class="section-subtitle">
        Compare airlines day by day throughout January 2018 with animated bar chart
    </p>
""", unsafe_allow_html=True)

# Create and display animated chart
try:
    fig_animation = create_animated_airline_chart(
        daily_airline_metrics,
        metric=animation_metric,
        selected_airlines=selected_airlines if selected_airlines else None
    )
    st.plotly_chart(fig_animation, use_container_width=True, key="animation")
    
    st.info("💡 **Tip**: Click the ▶️ play button to see how airlines compare over time!")
except Exception as e:
    st.error(f"Error creating animated chart: {e}")

st.markdown("---")

# ============================================
# VISUALIZATION 3: HIERARCHICAL SUNBURST
# ============================================

st.markdown("## 🌅 Flight Volume Hierarchy")

# Sunburst controls - positioned above the chart
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Get unique states for filter
    all_states = sorted(hierarchy_data['State'].unique().tolist())
    selected_state = st.selectbox(
        "Filter by State",
        options=['All States'] + all_states,
        key="selected_state",
        help="Filter the hierarchy to show only a specific state"
    )

# Convert 'All States' to None for the function
sunburst_state = None if selected_state == 'All States' else selected_state

st.markdown("""
    <p class="section-subtitle">
        Drill down through the hierarchy: State → City → Airport → Airline
    </p>
""", unsafe_allow_html=True)

# Create and display sunburst
try:
    fig_sunburst = create_sunburst(hierarchy_data, selected_state=sunburst_state)
    st.plotly_chart(fig_sunburst, use_container_width=True, key="sunburst")
    
    st.info("💡 **Tip**: Click on any segment to zoom in and explore the hierarchy!")
except Exception as e:
    st.error(f"Error creating sunburst chart: {e}")

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #0d9488; padding: 2rem 0;">
        <p>US Flight Analytics Dashboard • Data: January 2018 • Built with Streamlit + Plotly</p>
    </div>
""", unsafe_allow_html=True)
