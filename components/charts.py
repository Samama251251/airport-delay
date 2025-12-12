"""
Chart generation functions for Streamlit Flight Dashboard
All Plotly visualizations are defined here
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Color palette - teal/aviation theme with professional contrast
COLORS = {
    'background': '#f8fafc',        # slate-50 - neutral light background
    'surface': '#ffffff',           # pure white cards
    'surface_alt': '#f0fdf4',       # green-50 - alternating sections
    'primary': '#0d9488',           # teal-600 - main accent
    'primary_dark': '#0f766e',      # teal-700 - hover/active
    'primary_light': '#14b8a6',     # teal-500 - highlights
    'secondary': '#0ea5e9',         # sky-500 - secondary accent
    'accent': '#f59e0b',            # amber-500 - attention
    'success': '#10b981',           # emerald-500 - positive
    'warning': '#f59e0b',           # amber-500 - caution
    'danger': '#ef4444',            # red-500 - negative
    'text': '#134e4a',              # teal-900 - primary text
    'text_muted': '#14b8a6',        # teal-500 - muted text
    'grid': '#e2e8f0',              # slate-200 - subtle gridlines
    'border': '#99f6e4',            # teal-200 - card borders
    'sequential': px.colors.sequential.Tealgrn,
    'diverging': px.colors.diverging.RdYlGn_r,
    # Distinct colors for categorical data (airlines) - maximum distinguishability
    'chart_palette': [
        '#0d9488',  # teal
        '#0ea5e9',  # sky blue
        '#f59e0b',  # amber
        '#8b5cf6',  # violet
        '#ef4444',  # red
        '#06b6d4',  # cyan
        '#ec4899',  # pink
        '#84cc16',  # lime
        '#6366f1',  # indigo
        '#14b8a6',  # teal-light
    ]
}

# ============================================
# 1. US STATE CHOROPLETH MAP
# ============================================

def create_choropleth(state_metrics_df, metric='AvgDepDelay'):
    """
    Create interactive US state choropleth map
    
    Args:
        state_metrics_df: DataFrame with state-level metrics
        metric: Which metric to display ('AvgDepDelay', 'CancellationRate', 'FlightCount')
    """
    # Metric configuration
    metric_config = {
        'AvgDepDelay': {
            'title': 'Average Departure Delay by State',
            'color_scale': 'Teal',
            'labels': {'z': 'Avg Delay (min)'},
            'hover_suffix': ' min',
            'value_format': '.1f'
        },
        'CancellationRate': {
            'title': 'Flight Cancellation Rate by State',
            'color_scale': 'Teal',
            'labels': {'z': 'Cancel Rate (%)'},
            'hover_suffix': '%',
            'value_format': '.2f'
        },
        'FlightCount': {
            'title': 'Total Flight Volume by State',
            'color_scale': 'Teal',
            'labels': {'z': 'Total Flights'},
            'hover_suffix': ' flights',
            'value_format': ',.0f'
        }
    }
    
    config = metric_config.get(metric, metric_config['AvgDepDelay'])
    
    fig = px.choropleth(
        state_metrics_df,
        locations='StateCode',
        locationmode='USA-states',
        color=metric,
        scope='usa',
        color_continuous_scale=config['color_scale'],
        labels=config['labels'],
        hover_data={
            'StateCode': False,
            'StateName': True,
            'FlightCount': ':,',
            metric: f':{config["value_format"]}'
        }
    )
    
    fig.update_layout(
        title=dict(
            text=config['title'],
            font=dict(size=18, color=COLORS['text']),
            x=0.5,
            xanchor='center'
        ),
        geo=dict(
            bgcolor=COLORS['surface'],
            lakecolor=COLORS['background'],
            landcolor=COLORS['surface'],
            showcountries=False,
            showlakes=True
        ),
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        margin=dict(l=0, r=0, t=50, b=0),
        height=500,
        coloraxis_colorbar=dict(
            title=dict(text=config['labels']['z'], font=dict(size=12)),
            tickfont=dict(size=10)
        )
    )
    
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>' +
                     f'{config["labels"]["z"]}: %{{z:{config["value_format"]}}}{config["hover_suffix"]}<br>' +
                     'Total Flights: %{customdata[1]:,}<extra></extra>'
    )

    # Add labels for state name and metric value on the map
    fig.add_trace(go.Scattergeo(
        locations=state_metrics_df['StateCode'],
        locationmode='USA-states',
        text=state_metrics_df.apply(
            lambda row: f"{row['StateName']}<br>{row[metric]:{config['value_format']}}{config['hover_suffix']}",
            axis=1
        ),
        mode='text',
        textfont=dict(color='white', size=9, family='Arial', weight='bold'),
        hoverinfo='skip',
        showlegend=False
    ))
    
    return fig


# ============================================
# 2. ANIMATED AIRLINE PERFORMANCE (Bar Chart Race)
# ============================================

def create_animated_airline_chart(daily_airline_df, metric='FlightCount', selected_airlines=None):
    """
    Create animated bar chart showing daily airline performance over the month
    
    Args:
        daily_airline_df: DataFrame with daily airline metrics
        metric: Which metric to show ('FlightCount', 'AvgDepDelay', 'OnTimeRate')
        selected_airlines: List of airlines to include (None = all)
    """
    # Metric configuration
    metric_config = {
        'FlightCount': {
            'title': 'Daily Flight Volume by Airline',
            'subtitle': 'Number of flights operated each day',
            'x_label': 'Daily Flights',
            'format': ':,',
            'suffix': ' flights'
        },
        'AvgDepDelay': {
            'title': 'Average Departure Delay by Airline',
            'subtitle': 'Daily average delay in minutes',
            'x_label': 'Avg Delay (min)',
            'format': ':.1f',
            'suffix': ' min'
        },
        'OnTimeRate': {
            'title': 'On-Time Performance by Airline',
            'subtitle': 'Percentage of flights arriving within 15 minutes',
            'x_label': 'On-Time %',
            'format': ':.1f',
            'suffix': '%'
        }
    }
    
    config = metric_config.get(metric, metric_config['FlightCount'])
    
    # Filter airlines if specified
    df = daily_airline_df.copy()
    if selected_airlines and len(selected_airlines) > 0:
        df = df[df['Airline'].isin(selected_airlines)]
    
    # Calculate x-axis range based on filtered data (with 10% padding)
    max_value = df[metric].max()
    x_range_max = max_value * 1.1 if max_value > 0 else 100
    
    # Sort data - for delay/cancellation, descending shows worst performers at top
    ascending_metric = metric in ['FlightCount', 'OnTimeRate']
    df = df.sort_values(['Day', metric], ascending=[True, not ascending_metric])
    
    # Create animated bar chart
    fig = px.bar(
        df,
        x=metric,
        y='Airline',
        color='Airline',
        animation_frame='Day',
        orientation='h',
        color_discrete_sequence=COLORS['chart_palette'],
        hover_data={
            'Airline': False,
            'Day': True,
            'FlightCount': ':,',
            'AvgDepDelay': ':.1f',
            'OnTimeRate': ':.1f',
            'CancellationRate': ':.2f'
        }
    )
    
    # Update layout for clean appearance
    fig.update_layout(
        title=dict(
            text=f"{config['title']}<br><sub>{config['subtitle']}</sub>",
            font=dict(size=16, color=COLORS['text']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text=config['x_label'], font=dict(color=COLORS['text'])),
            gridcolor=COLORS['grid'],
            tickfont=dict(color=COLORS['text']),
            range=[0, x_range_max]  # Fixed range based on filtered data
        ),
        yaxis=dict(
            title=dict(text='', font=dict(color=COLORS['text'])),
            categoryorder='total ascending',
            tickfont=dict(color=COLORS['text'], size=10)
        ),
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['surface'],
        font=dict(color=COLORS['text']),
        height=500,
        showlegend=False,
        margin=dict(l=150, r=20, t=80, b=60)
    )
    
    # Update hover template
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>' +
                     f'{config["x_label"]}: %{{x{config["format"]}}}{config["suffix"]}<br>' +
                     'Day: %{customdata[0]}<br>' +
                     'Daily Flights: %{customdata[1]:,}<br>' +
                     'Avg Delay: %{customdata[2]:.1f} min<br>' +
                     'On-Time: %{customdata[3]:.1f}%<br>' +
                     'Cancellation: %{customdata[4]:.2f}%<extra></extra>'
    )
    
    # Customize animation settings
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 400
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 150
    
    # Style the animation slider
    if fig.layout.sliders:
        fig.layout.sliders[0].currentvalue = dict(
            prefix="Day: ",
            font=dict(color=COLORS['text'], size=14)
        )
        fig.layout.sliders[0].font = dict(color=COLORS['text'])
    
    return fig


# ============================================
# 3. HIERARCHICAL SUNBURST
# ============================================

def create_sunburst(hierarchy_df, selected_state=None):
    """
    Create interactive sunburst chart
    Hierarchy: State → City → Airport → Airline
    
    Args:
        hierarchy_df: DataFrame with hierarchical data
        selected_state: Optional state filter
    """
    # Filter by state if selected
    if selected_state:
        hierarchy_df = hierarchy_df[hierarchy_df['State'] == selected_state]
    
    # Vibrant color scale with high contrast - low delays (blue/green) to high delays (orange/red)
    vibrant_scale = [
        [0.0, '#0891b2'],   # cyan-600 (low delay - excellent)
        [0.2, '#0d9488'],   # teal-600 (good)
        [0.4, '#14b8a6'],   # teal-500 (moderate)
        [0.6, '#fbbf24'],   # amber-400 (fair)
        [0.8, '#f97316'],   # orange-500 (poor)
        [1.0, '#dc2626']    # red-600 (very poor)
    ]
    
    fig = px.sunburst(
        hierarchy_df,
        path=['State', 'City', 'Airport', 'Airline'],
        values='FlightCount',
        color='AvgDelay',
        color_continuous_scale=vibrant_scale,
        range_color=[0, 40],  # Set realistic delay range: 0-40 minutes
        hover_data={
            'FlightCount': ':,',
            'AvgDelay': ':.1f'
        }
    )
    
    subtitle = 'Click to drill down: State → City → Airport → Airline'
    if selected_state:
        subtitle = f'Filtered: {selected_state}'
    
    fig.update_layout(
        title=dict(
            text=f'Flight Volume Hierarchy<br><sub>{subtitle}</sub>',
            font=dict(size=18, color=COLORS['text']),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], size=13, family="'Inter', sans-serif"),
        height=700,
        margin=dict(t=60, l=10, r=120, b=10),
        coloraxis_colorbar=dict(
            title=dict(text="Avg Delay<br>(minutes)", font=dict(size=12, color=COLORS['text'])),
            tickfont=dict(size=11, color=COLORS['text']),
            len=0.5,
            thickness=15,
            x=1.0,
            tickmode='linear',
            tick0=0,
            dtick=10  # Show ticks at 0, 10, 20, 30, 40
        )
    )
    
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>' +
                     'Flights: %{value:,}<br>' +
                     'Avg Delay: %{color:.1f} min<extra></extra>',
        textinfo='label+percent entry',
        textfont=dict(size=15, color='white', family="'Inter', sans-serif", weight=600),
        marker=dict(
            line=dict(color='white', width=2.5)
        ),
        insidetextorientation='radial'
    )
    
    return fig
