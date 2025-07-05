"""
Replay Dashboard for GhostLAN SimWorld
Match replay with play/pause/seek controls and visualization
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import requests
import json
import time

API_URL = "http://localhost:8000"

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("GhostLAN SimWorld Match Replay"),
    html.Div([
        html.H3("Recorded Matches"),
        dcc.Dropdown(id="match-dropdown", placeholder="Select a match to replay"),
        html.Button("Load Match", id="load-match-btn", n_clicks=0),
        html.Button("Delete Match", id="delete-match-btn", n_clicks=0),
        html.Div(id="match-info"),
    ]),
    html.Hr(),
    html.Div([
        html.H3("Replay Controls"),
        html.Button("⏮️", id="rewind-btn", n_clicks=0),
        html.Button("⏯️", id="play-pause-btn", n_clicks=0),
        html.Button("⏭️", id="fast-forward-btn", n_clicks=0),
        dcc.Slider(id="replay-slider", min=0, max=100, step=1, value=0, marks={}),
        html.Div(id="replay-status"),
    ]),
    html.Hr(),
    html.Div([
        html.H3("Match Visualization"),
        dcc.Graph(id="replay-graph"),
        dcc.Interval(id='replay-interval', interval=100, n_intervals=0, disabled=True),
    ]),
    html.Hr(),
    html.Div([
        html.H3("Export"),
        html.Button("Export as JSON", id="export-json-btn", n_clicks=0),
        html.Button("Export as CSV", id="export-csv-btn", n_clicks=0),
        html.Div(id="export-status"),
    ]),
])

@app.callback(
    Output("match-dropdown", "options"),
    Output("match-dropdown", "value"),
    Input("load-match-btn", "n_clicks"),
    Input("delete-match-btn", "n_clicks"),
    State("match-dropdown", "value")
)
def update_match_list(load_clicks, delete_clicks, selected_match):
    try:
        matches = requests.get(f"{API_URL}/replay/matches").json()
        options = [{"label": f"{m['match_id']} - {m['start_time']}", "value": m['match_id']} for m in matches]
        
        # Delete match if button clicked
        if delete_clicks and selected_match:
            requests.delete(f"{API_URL}/replay/matches/{selected_match}")
            return options, None
            
        return options, selected_match
    except:
        return [], None

@app.callback(
    Output("match-info", "children"),
    Output("replay-slider", "max"),
    Output("replay-slider", "marks"),
    Input("load-match-btn", "n_clicks"),
    State("match-dropdown", "value")
)
def load_match_info(load_clicks, selected_match):
    if not selected_match:
        return "No match selected", 100, {}
    
    try:
        match_data = requests.get(f"{API_URL}/replay/matches/{selected_match}").json()
        events = match_data.get('events', [])
        summary = match_data.get('summary', {})
        
        # Create slider marks
        if events:
            max_tick = max(e.get('tick', 0) for e in events)
            marks = {i: str(i) for i in range(0, max_tick + 1, max_tick // 10)}
        else:
            max_tick = 100
            marks = {}
        
        info = f"""
        **Match ID:** {selected_match}
        **Events:** {len(events)}
        **Summary:** {json.dumps(summary, indent=2)}
        """
        
        return info, max_tick, marks
    except:
        return "Error loading match", 100, {}

@app.callback(
    Output("replay-status", "children"),
    Output("replay-interval", "disabled"),
    Input("play-pause-btn", "n_clicks"),
    State("replay-interval", "disabled")
)
def toggle_playback(n_clicks, is_disabled):
    if n_clicks:
        return "Playing" if is_disabled else "Paused", not is_disabled
    return "Paused", True

@app.callback(
    Output("replay-graph", "figure"),
    Input("replay-slider", "value"),
    Input("replay-interval", "n_intervals"),
    State("match-dropdown", "value")
)
def update_replay_visualization(slider_value, interval_value, selected_match):
    if not selected_match:
        return go.Figure().add_annotation(text="No match loaded", x=0.5, y=0.5, showarrow=False)
    
    try:
        match_data = requests.get(f"{API_URL}/replay/matches/{selected_match}").json()
        events = match_data.get('events', [])
        
        if not events:
            return go.Figure().add_annotation(text="No events in match", x=0.5, y=0.5, showarrow=False)
        
        # Filter events up to current tick
        current_tick = slider_value if slider_value > 0 else (interval_value or 0)
        filtered_events = [e for e in events if e.get('tick', 0) <= current_tick]
        
        # Create visualization based on event types
        fig = go.Figure()
        
        # Plot agent positions
        agent_events = [e for e in filtered_events if e.get('type') == 'agent_action']
        if agent_events:
            x_pos = [e.get('data', {}).get('position', [0, 0, 0])[0] for e in agent_events]
            z_pos = [e.get('data', {}).get('position', [0, 0, 0])[2] for e in agent_events]
            agent_ids = [e.get('data', {}).get('agent_id', 'Unknown') for e in agent_events]
            
            fig.add_trace(go.Scatter(
                x=x_pos, y=z_pos,
                mode='markers+text',
                text=agent_ids,
                name='Agent Positions',
                marker=dict(size=10, color='blue')
            ))
        
        fig.update_layout(
            title=f"Match Replay - Tick {current_tick}",
            xaxis_title="X Position",
            yaxis_title="Z Position",
            height=500
        )
        
        return fig
    except:
        return go.Figure().add_annotation(text="Error loading visualization", x=0.5, y=0.5, showarrow=False)

@app.callback(
    Output("export-status", "children"),
    Input("export-json-btn", "n_clicks"),
    Input("export-csv-btn", "n_clicks"),
    State("match-dropdown", "value")
)
def export_match(json_clicks, csv_clicks, selected_match):
    if not selected_match:
        return "No match selected"
    
    if json_clicks:
        try:
            response = requests.get(f"{API_URL}/replay/matches/{selected_match}/export?format=json")
            return f"✅ JSON exported successfully! Size: {len(response.content)} bytes"
        except:
            return "❌ Failed to export JSON"
    
    if csv_clicks:
        try:
            response = requests.get(f"{API_URL}/replay/matches/{selected_match}/export?format=csv")
            return f"✅ CSV exported successfully! Size: {len(response.content)} bytes"
        except:
            return "❌ Failed to export CSV"
    
    return "Click export buttons to download match data"

if __name__ == "__main__":
    app.run_server(debug=True, port=8080) 