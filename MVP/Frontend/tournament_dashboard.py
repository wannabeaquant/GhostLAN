"""
Tournament Dashboard for GhostLAN SimWorld
Run multiple matches, show brackets, and display leaderboards
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import requests
import time

API_URL = "http://localhost:8000"

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("GhostLAN SimWorld Tournament Mode"),
    html.Button("Start Tournament", id="start-tournament-btn"),
    html.Div(id="tournament-status"),
    html.Hr(),
    html.H2("Bracket"),
    dcc.Graph(id="bracket-graph"),
    html.H2("Leaderboard"),
    dcc.Interval(id='interval-component', interval=3000, n_intervals=0),
    html.Div(id="leaderboard-table"),
])

@app.callback(
    Output("tournament-status", "children"),
    Output("bracket-graph", "figure"),
    Output("leaderboard-table", "children"),
    Input("start-tournament-btn", "n_clicks"),
    Input('interval-component', 'n_intervals'),
    State("tournament-status", "children")
)
def update_tournament(n_clicks, n_intervals, status):
    # Start tournament on button click
    if n_clicks and (not status or "started" not in status):
        # Call backend to start tournament (stub)
        requests.post(f"{API_URL}/tournament/start")
        status = "Tournament started!"
    else:
        status = status or "Waiting to start..."
    # Get bracket (stub)
    bracket = requests.get(f"{API_URL}/tournament/bracket").json()
    fig = go.Figure()
    if bracket:
        for match in bracket.get('matches', []):
            fig.add_trace(go.Scatter(
                x=[match['round']],
                y=[match['match_id']],
                text=[f"{match['team_a']} vs {match['team_b']}"]
            ))
    fig.update_layout(title="Tournament Bracket", xaxis_title="Round", yaxis_title="Match")
    # Get leaderboard
    leaderboard = requests.get(f"{API_URL}/tournament/leaderboard").json()
    table = html.Table([
        html.Tr([html.Th("Player"), html.Th("Wins"), html.Th("Score")])
    ] + [
        html.Tr([html.Td(row['player']), html.Td(row['wins']), html.Td(row['score'])]) for row in leaderboard
    ])
    return status, fig, table

if __name__ == "__main__":
    app.run_server(debug=True, port=8060) 