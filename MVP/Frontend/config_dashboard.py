"""
Configuration Dashboard for GhostLAN SimWorld
Live configuration of simulation parameters
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import requests
import json

API_URL = "http://localhost:8000"

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("GhostLAN SimWorld Configuration"),
    html.Div([
        html.H3("Simulation Parameters"),
        html.Label("Number of Players:"),
        dcc.Slider(id="num-players", min=2, max=20, step=2, value=10, marks={i: str(i) for i in range(2, 21, 2)}),
        html.Br(),
        html.Label("Cheat Probability:"),
        dcc.Slider(id="cheat-prob", min=0, max=1, step=0.1, value=0.3, marks={i/10: f"{i*10}%" for i in range(0, 11)}),
        html.Br(),
        html.Label("Match Duration (seconds):"),
        dcc.Slider(id="match-duration", min=60, max=600, step=30, value=300, marks={i: f"{i}s" for i in range(60, 601, 120)}),
        html.Br(),
        html.Label("Tick Rate (FPS):"),
        dcc.Slider(id="tick-rate", min=30, max=120, step=10, value=60, marks={i: str(i) for i in range(30, 121, 30)}),
        html.Br(),
        html.H3("Network Conditions"),
        html.Label("Packet Loss (%):"),
        dcc.Slider(id="packet-loss", min=0, max=10, step=0.5, value=2, marks={i: f"{i}%" for i in range(0, 11, 2)}),
        html.Br(),
        html.Label("Latency (ms):"),
        dcc.Slider(id="latency", min=1, max=100, step=5, value=15, marks={i: f"{i}ms" for i in range(0, 101, 20)}),
        html.Br(),
        html.Label("Jitter (ms):"),
        dcc.Slider(id="jitter", min=0, max=20, step=1, value=5, marks={i: f"{i}ms" for i in range(0, 21, 5)}),
        html.Br(),
        html.Label("Bandwidth (Mbps):"),
        dcc.Slider(id="bandwidth", min=10, max=1000, step=10, value=100, marks={i: f"{i}Mbps" for i in range(0, 1001, 200)}),
        html.Br(),
        html.Button("Apply Configuration", id="apply-config-btn", n_clicks=0),
        html.Div(id="config-status"),
    ]),
    html.Hr(),
    html.H3("Current Configuration"),
    html.Pre(id="current-config"),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
])

@app.callback(
    Output("config-status", "children"),
    Output("current-config", "children"),
    Input("apply-config-btn", "n_clicks"),
    Input('interval-component', 'n_intervals'),
    State("num-players", "value"),
    State("cheat-prob", "value"),
    State("match-duration", "value"),
    State("tick-rate", "value"),
    State("packet-loss", "value"),
    State("latency", "value"),
    State("jitter", "value"),
    State("bandwidth", "value")
)
def update_config(n_clicks, n_intervals, num_players, cheat_prob, match_duration, tick_rate, packet_loss, latency, jitter, bandwidth):
    status = ""
    if n_clicks > 0:
        config = {
            "num_players": num_players,
            "cheat_probability": cheat_prob,
            "match_duration": match_duration,
            "tick_rate": tick_rate,
            "network_conditions": {
                "packet_loss": packet_loss / 100,
                "latency": latency,
                "jitter": jitter,
                "bandwidth": bandwidth
            }
        }
        try:
            response = requests.post(f"{API_URL}/config", json=config)
            if response.status_code == 200:
                status = "✅ Configuration applied successfully!"
            else:
                status = "❌ Failed to apply configuration"
        except:
            status = "❌ Could not connect to API"
    else:
        status = "Click 'Apply Configuration' to update settings"
    
    # Get current config
    try:
        current = requests.get(f"{API_URL}/config").json()
        current_str = json.dumps(current, indent=2)
    except:
        current_str = "Could not fetch current configuration"
    
    return status, current_str

if __name__ == "__main__":
    app.run_server(debug=True, port=8070) 