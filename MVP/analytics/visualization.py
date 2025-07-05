"""
Advanced Visualization for GhostLAN SimWorld
2D/3D match replay, heatmaps, network topology, and real-time charts
"""

import logging
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class AdvancedVisualization:
    """Advanced visualization engine for GhostLAN SimWorld"""
    
    def __init__(self):
        self.match_replay_data = []
        self.heatmap_data = []
        self.network_topology = {}
        self.chart_data = {
            'performance': [],
            'detections': [],
            'voice_activity': []
        }
        
    def create_match_replay_2d(self, agents_data: List[Dict[str, Any]], 
                              map_bounds: tuple, obstacles: List[Dict[str, Any]]) -> go.Figure:
        """Create 2D match replay visualization"""
        fig = go.Figure()
        
        # Add map boundaries
        x_min, x_max, z_min, z_max = map_bounds
        fig.add_shape(
            type="rect",
            x0=x_min, y0=z_min, x1=x_max, y1=z_max,
            line=dict(color="black", width=2),
            fillcolor="rgba(0,0,0,0)"
        )
        
        # Add obstacles
        for obstacle in obstacles:
            pos = obstacle['position']
            size = obstacle['size']
            fig.add_shape(
                type="rect",
                x0=pos[0] - size[0]/2, y0=pos[2] - size[2]/2,
                x1=pos[0] + size[0]/2, y1=pos[2] + size[2]/2,
                line=dict(color="gray", width=1),
                fillcolor="rgba(100,100,100,0.3)"
            )
        
        # Add agents
        team_a_x, team_a_z = [], []
        team_b_x, team_b_z = [], []
        team_a_names, team_b_names = [], []
        
        for agent in agents_data:
            pos = agent.get('position', (0, 0, 0))
            team = agent.get('team', '')
            name = agent.get('id', 'Unknown')
            
            if 'TeamA' in name:
                team_a_x.append(pos[0])
                team_a_z.append(pos[2])
                team_a_names.append(name)
            else:
                team_b_x.append(pos[0])
                team_b_z.append(pos[2])
                team_b_names.append(name)
        
        # Plot team A (blue)
        fig.add_trace(go.Scatter(
            x=team_a_x, y=team_a_z,
            mode='markers+text',
            name='Team A',
            text=team_a_names,
            textposition="top center",
            marker=dict(size=15, color='blue', symbol='circle'),
            hovertemplate='<b>%{text}</b><br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>'
        ))
        
        # Plot team B (red)
        fig.add_trace(go.Scatter(
            x=team_b_x, y=team_b_z,
            mode='markers+text',
            name='Team B',
            text=team_b_names,
            textposition="top center",
            marker=dict(size=15, color='red', symbol='square'),
            hovertemplate='<b>%{text}</b><br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>'
        ))
        
        fig.update_layout(
            title="GhostLAN SimWorld - 2D Match Replay",
            xaxis_title="X Position",
            yaxis_title="Z Position",
            xaxis=dict(range=[x_min-10, x_max+10]),
            yaxis=dict(range=[z_min-10, z_max+10]),
            showlegend=True,
            height=600
        )
        
        return fig
        
    def create_heatmap(self, heatmap_data: Dict[str, Any]) -> go.Figure:
        """Create player position heatmap"""
        x = heatmap_data.get('x', [])
        y = heatmap_data.get('y', [])
        intensity = heatmap_data.get('intensity', [])
        
        # Create 2D histogram
        fig = go.Figure(data=go.Histogram2d(
            x=x, y=y,
            nbinsx=20, nbinsy=20,
            colorscale='Viridis',
            showscale=True
        ))
        
        fig.update_layout(
            title="Player Position Heatmap",
            xaxis_title="X Position",
            yaxis_title="Z Position",
            height=500
        )
        
        return fig
        
    def create_network_topology(self, network_data: Dict[str, Any]) -> go.Figure:
        """Create network topology visualization"""
        # Simulate network nodes and connections
        nodes = []
        edges = []
        
        # Add server node
        nodes.append(dict(id="Server", x=0, y=0, size=20, color="green"))
        
        # Add client nodes
        for i in range(10):
            angle = i * 36  # Distribute in a circle
            x = 50 * np.cos(np.radians(angle))
            y = 50 * np.sin(np.radians(angle))
            nodes.append(dict(
                id=f"Client_{i+1}",
                x=x, y=y,
                size=15,
                color="blue" if i < 5 else "red"
            ))
            edges.append(dict(
                from_node="Server",
                to_node=f"Client_{i+1}",
                latency=network_data.get('latency', 15) + np.random.uniform(-5, 5)
            ))
        
        # Create network graph
        fig = go.Figure()
        
        # Add edges
        for edge in edges:
            from_node = next(n for n in nodes if n['id'] == edge['from_node'])
            to_node = next(n for n in nodes if n['id'] == edge['to_node'])
            
            fig.add_trace(go.Scatter(
                x=[from_node['x'], to_node['x']],
                y=[from_node['y'], to_node['y']],
                mode='lines',
                line=dict(color='gray', width=1),
                showlegend=False,
                hovertemplate=f"Latency: {edge['latency']:.1f}ms<extra></extra>"
            ))
        
        # Add nodes
        for node in nodes:
            fig.add_trace(go.Scatter(
                x=[node['x']], y=[node['y']],
                mode='markers+text',
                text=[node['id']],
                textposition="top center",
                marker=dict(
                    size=node['size'],
                    color=node['color'],
                    symbol='circle'
                ),
                name=node['id'],
                hovertemplate=f"<b>{node['id']}</b><extra></extra>"
            ))
        
        fig.update_layout(
            title="Network Topology",
            xaxis_title="X",
            yaxis_title="Y",
            showlegend=True,
            height=500
        )
        
        return fig
        
    def create_performance_dashboard(self, performance_data: Dict[str, Any]) -> go.Figure:
        """Create real-time performance dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Network Health', 'FPS', 'CPU Usage', 'Memory Usage'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Network Health
        if 'network_health' in performance_data:
            nh = performance_data['network_health']
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=nh.get('current', 0) * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Network Health (%)"},
                    gauge={'axis': {'range': [None, 100]},
                           'bar': {'color': "darkblue"},
                           'steps': [{'range': [0, 50], 'color': "lightgray"},
                                    {'range': [50, 80], 'color': "yellow"},
                                    {'range': [80, 100], 'color': "green"}]},
                    delta={'reference': nh.get('average', 0) * 100}
                ),
                row=1, col=1
            )
        
        # FPS
        if 'fps' in performance_data:
            fps = performance_data['fps']
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=fps.get('current', 60),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "FPS"},
                    gauge={'axis': {'range': [0, 120]},
                           'bar': {'color': "darkgreen"},
                           'steps': [{'range': [0, 30], 'color': "red"},
                                    {'range': [30, 60], 'color': "yellow"},
                                    {'range': [60, 120], 'color': "green"}]},
                    delta={'reference': fps.get('average', 60)}
                ),
                row=1, col=2
            )
        
        # CPU Usage
        if 'cpu_usage' in performance_data:
            cpu = performance_data['cpu_usage']
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=cpu.get('current', 0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "CPU Usage (%)"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "darkred"},
                           'steps': [{'range': [0, 50], 'color': "green"},
                                    {'range': [50, 80], 'color': "yellow"},
                                    {'range': [80, 100], 'color': "red"}]},
                    delta={'reference': cpu.get('average', 0)}
                ),
                row=2, col=1
            )
        
        # Memory Usage
        if 'memory_usage' in performance_data:
            mem = performance_data['memory_usage']
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=mem.get('current', 0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Memory Usage (%)"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "purple"},
                           'steps': [{'range': [0, 50], 'color': "green"},
                                    {'range': [50, 80], 'color': "yellow"},
                                    {'range': [80, 100], 'color': "red"}]},
                    delta={'reference': mem.get('average', 0)}
                ),
                row=2, col=2
            )
        
        fig.update_layout(height=600, title_text="Performance Dashboard")
        return fig
        
    def create_detection_timeline(self, detections: List[Dict[str, Any]]) -> go.Figure:
        """Create cheat detection timeline"""
        if not detections:
            return go.Figure().add_annotation(
                text="No detections yet",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # Process detection data
        timestamps = []
        rules = []
        confidences = []
        agents = []
        
        for detection in detections:
            timestamps.append(detection.get('timestamp', datetime.now()))
            rules.append(detection.get('rule', 'unknown'))
            confidences.append(detection.get('confidence', 0) * 100)
            agents.append(detection.get('agent_id', 'unknown'))
        
        fig = go.Figure()
        
        # Create scatter plot
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=confidences,
            mode='markers+lines',
            text=agents,
            hovertemplate='<b>%{text}</b><br>Rule: %{customdata}<br>Confidence: %{y:.1f}%<extra></extra>',
            customdata=rules,
            marker=dict(
                size=10,
                color=confidences,
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Confidence %")
            )
        ))
        
        fig.update_layout(
            title="Cheat Detection Timeline",
            xaxis_title="Time",
            yaxis_title="Detection Confidence (%)",
            height=400
        )
        
        return fig
        
    def create_voice_activity_chart(self, voice_data: Dict[str, Any]) -> go.Figure:
        """Create voice activity visualization"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Voice Packet Activity', 'Voice Quality Over Time'),
            vertical_spacing=0.1
        )
        
        # Voice packet activity
        if 'voice_events' in voice_data:
            events = voice_data['voice_events']
            if events:
                timestamps = [e.get('timestamp', datetime.now()) for e in events]
                packet_sizes = [e.get('packet_size', 0) for e in events]
                qualities = [e.get('quality', 0) for e in events]
                
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=packet_sizes,
                        mode='markers',
                        name='Packet Size',
                        marker=dict(size=5, color='blue')
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=qualities,
                        mode='lines',
                        name='Voice Quality',
                        line=dict(color='green')
                    ),
                    row=2, col=1
                )
        
        fig.update_layout(height=600, title_text="Voice Activity Analysis")
        return fig
        
    def create_3d_match_replay(self, agents_data: List[Dict[str, Any]]) -> go.Figure:
        """Create 3D match replay visualization"""
        fig = go.Figure()
        
        # Separate teams
        team_a_x, team_a_y, team_a_z = [], [], []
        team_b_x, team_b_y, team_b_z = [], [], []
        team_a_names, team_b_names = [], []
        
        for agent in agents_data:
            pos = agent.get('position', (0, 0, 0))
            name = agent.get('id', 'Unknown')
            
            if 'TeamA' in name:
                team_a_x.append(pos[0])
                team_a_y.append(pos[1])
                team_a_z.append(pos[2])
                team_a_names.append(name)
            else:
                team_b_x.append(pos[0])
                team_b_y.append(pos[1])
                team_b_z.append(pos[2])
                team_b_names.append(name)
        
        # Add team A
        fig.add_trace(go.Scatter3d(
            x=team_a_x, y=team_a_y, z=team_a_z,
            mode='markers+text',
            name='Team A',
            text=team_a_names,
            marker=dict(size=8, color='blue', symbol='circle'),
            hovertemplate='<b>%{text}</b><br>Position: (%{x:.1f}, %{y:.1f}, %{z:.1f})<extra></extra>'
        ))
        
        # Add team B
        fig.add_trace(go.Scatter3d(
            x=team_b_x, y=team_b_y, z=team_b_z,
            mode='markers+text',
            name='Team B',
            text=team_b_names,
            marker=dict(size=8, color='red', symbol='square'),
            hovertemplate='<b>%{text}</b><br>Position: (%{x:.1f}, %{y:.1f}, %{z:.1f})<extra></extra>'
        ))
        
        fig.update_layout(
            title="GhostLAN SimWorld - 3D Match Replay",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y", 
                zaxis_title="Z",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            height=600
        )
        
        return fig 