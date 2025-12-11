# Quick Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip package manager

## Installation Steps

### 1. Navigate to the project directory
```bash
cd /Users/samama/Sem5/DV/project2/flight-dashboard-streamlit
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
```

### 3. Activate the virtual environment
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the dashboard
```bash
streamlit run app.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

## Troubleshooting

### Port already in use
If port 8501 is already in use, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

### Data not found error
Ensure you're in the correct directory and the `data/aggregated/` folder contains all CSV files.

### Import errors
Make sure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```

## Features to Try

1. **Sidebar Controls**: Use the sidebar on the left to:
   - Change the map metric (Delay, Cancellation Rate, Flight Volume)
   - Select animation metric and filter airlines
   - Filter sunburst chart by state

2. **Interactive Elements**:
   - Hover over any chart element for details
   - Click play ▶️ on the animated bar chart
   - Click segments in the sunburst to drill down

3. **Performance**: All data is cached for fast loading

## Next Steps

- Explore different metric combinations
- Compare specific airlines in the animation
- Drill down into specific states/cities in the sunburst

---

Enjoy exploring the flight data! ✈️
