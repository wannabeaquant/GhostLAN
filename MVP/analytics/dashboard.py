"""
Analytics Dashboard for GhostLAN SimWorld
Visualizes match events, detections, and stats using Plotly Dash
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import requests
import threading
import time

API_URL = "http://localhost:8000"

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("GhostLAN SimWorld Dashboard"),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0),
    html.Div([
        html.Div([
            html.H3("Match State"),
            html.Pre(id='match-state', style={"background": "#f4f4f4", "padding": "10px"})
        ], style={"width": "32%", "display": "inline-block", "verticalAlign": "top"}),
        html.Div([
            html.H3("Anti-Cheat Detections"),
            html.Pre(id='detections', style={"background": "#fff0f0", "padding": "10px"})
        ], style={"width": "32%", "display": "inline-block", "verticalAlign": "top"}),
        html.Div([
            html.H3("Analytics"),
            html.Pre(id='analytics', style={"background": "#f0fff0", "padding": "10px"})
        ], style={"width": "32%", "display": "inline-block", "verticalAlign": "top"}),
    ]),
    html.Hr(),
    html.H2("Event Timeline"),
    dcc.Graph(id='event-timeline'),
])

@app.callback(
    Output('match-state', 'children'),
    Output('detections', 'children'),
    Output('analytics', 'children'),
    Output('event-timeline', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    try:
        state = requests.get(f"{API_URL}/state").json()
    except Exception:
        state = {"error": "No data"}
    try:
        detections = requests.get(f"{API_URL}/detections").json()
    except Exception:
        detections = []
    try:
        analytics = requests.get(f"{API_URL}/analytics").json()
    except Exception:
        analytics = {}
    # Timeline plot (dummy for now)
    try:
        events = requests.get(f"{API_URL}/state").json().get('events', [])
        ticks = [e.get('tick', 0) for e in events]
        types = [e.get('type', '') for e in events]
        fig = go.Figure([go.Scatter(x=ticks, y=types, mode='markers')])
        fig.update_layout(title="Event Timeline", xaxis_title="Tick", yaxis_title="Event Type")
    except Exception:
        fig = go.Figure()
    return (
        str(state),
        str(detections),
        str(analytics),
        fig
    )

def run_dashboard():
    app.run_server(debug=True, port=8050)

if __name__ == "__main__":
    run_dashboard() 