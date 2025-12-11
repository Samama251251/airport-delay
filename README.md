# US Flight Analytics Dashboard - Streamlit Version

Interactive dashboard for analyzing US flight data from January 2018.

## Features

### Three Interactive Visualizations

1. **🗺️ US State Choropleth Map**
   - View flight metrics by state (Average Delay, Cancellation Rate, Flight Volume)
   - Color-coded map with interactive hover details
   - Real-time metric switching

2. **📊 Animated Airline Bar Chart Race**
   - Watch daily airline performance throughout the month
   - Animated timeline showing how airlines compare day-by-day
   - Filter by specific airlines or view all
   - Multiple metrics: Flight Count, Avg Delay, On-Time %, Cancellation %

3. **🌅 Hierarchical Sunburst Chart**
   - Drill down through the hierarchy: State → City → Airport → Airline
   - Interactive exploration with click-to-zoom
   - Color-coded by average delay
   - Optional state filtering

## Installation

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

Launch the Streamlit app:
```bash
streamlit run app.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

## Data

The dashboard uses pre-aggregated data from January 2018 US flight records:
- `state_metrics.csv` - State-level flight metrics
- `daily_airline_metrics.csv` - Daily airline performance
- `hierarchy_data.csv` - Hierarchical flight data (State/City/Airport/Airline)
- `summary_stats.csv` - Overall KPI metrics
- `airline_metrics.csv` - Airline-level aggregates

## Project Structure

```
flight-dashboard-streamlit/
├── app.py                      # Main Streamlit application
├── components/
│   ├── __init__.py
│   └── charts.py              # Plotly chart generation functions
├── data/
│   └── aggregated/            # Pre-processed CSV files
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Technologies

- **Streamlit** - Dashboard framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **Python 3.8+**

## Usage Tips

- Use the **sidebar** to control all visualizations
- The **animated bar chart** has a play button - click it to watch the animation
- **Click on states** in the map to explore specific regions
- **Click segments** in the sunburst chart to drill down into the hierarchy
- All charts support **hover** to see detailed information

## Performance

The dashboard uses Streamlit's caching (`@st.cache_data`) to efficiently load data, ensuring fast performance even with multiple visualizations.

## Comparison with Dash Version

This Streamlit implementation provides the same three core visualizations as the Dash version:
- Same data processing and visualization logic
- Simplified deployment with Streamlit's built-in features
- Cleaner sidebar-based controls
- Automatic responsive design

---

**Built with ❤️ using Streamlit + Plotly**
