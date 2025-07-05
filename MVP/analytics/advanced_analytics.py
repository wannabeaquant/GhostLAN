"""
Advanced Analytics for GhostLAN SimWorld
Performance metrics, player rankings, match history, and sophisticated analysis
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import sqlite3
from collections import defaultdict

logger = logging.getLogger(__name__)

class AdvancedAnalytics:
    """Advanced analytics engine for GhostLAN SimWorld"""
    
    def __init__(self, db_path: str = "analytics.db"):
        self.db_path = db_path
        self.conn = None
        self.match_history = []
        self.player_rankings = defaultdict(lambda: {
            'total_matches': 0,
            'wins': 0,
            'kills': 0,
            'deaths': 0,
            'accuracy': 0.0,
            'avg_score': 0.0,
            'cheat_detections': 0
        })
        self.performance_metrics = {
            'network_health': [],
            'fps_history': [],
            'cpu_usage': [],
            'memory_usage': []
        }
        
    async def initialize(self):
        """Initialize advanced analytics"""
        logger.info("📊 Initializing Advanced Analytics...")
        self.conn = sqlite3.connect(self.db_path)
        self._create_advanced_tables()
        
    def _create_advanced_tables(self):
        """Create advanced analytics tables"""
        cursor = self.conn.cursor()
        
        # Player statistics table
        cursor.execute('''CREATE TABLE IF NOT EXISTS player_stats (
            player_id TEXT PRIMARY KEY,
            total_matches INTEGER,
            wins INTEGER,
            kills INTEGER,
            deaths INTEGER,
            accuracy REAL,
            avg_score REAL,
            cheat_detections INTEGER,
            last_updated TEXT
        )''')
        
        # Match history table
        cursor.execute('''CREATE TABLE IF NOT EXISTS match_history (
            match_id TEXT PRIMARY KEY,
            start_time TEXT,
            end_time TEXT,
            duration REAL,
            team_a_score INTEGER,
            team_b_score INTEGER,
            winner TEXT,
            cheaters_detected INTEGER,
            total_events INTEGER,
            network_issues INTEGER
        )''')
        
        # Performance metrics table
        cursor.execute('''CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            network_health REAL,
            fps REAL,
            cpu_usage REAL,
            memory_usage REAL
        )''')
        
        self.conn.commit()
        
    def process_match_end(self, match_data: Dict[str, Any]):
        """Process match end data and update analytics"""
        match_id = f"match_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Update match history
        match_record = {
            'match_id': match_id,
            'start_time': match_data.get('start_time', datetime.now().isoformat()),
            'end_time': datetime.now().isoformat(),
            'duration': match_data.get('match_duration', 0),
            'team_a_score': match_data.get('team_a_score', 0),
            'team_b_score': match_data.get('team_b_score', 0),
            'winner': match_data.get('winner', 'Unknown'),
            'cheaters_detected': match_data.get('cheaters_detected', 0),
            'total_events': match_data.get('total_events', 0),
            'network_issues': match_data.get('network_issues', 0)
        }
        
        self.match_history.append(match_record)
        self._save_match_to_db(match_record)
        
        # Update player rankings
        self._update_player_rankings(match_data)
        
        logger.info(f"📈 Match {match_id} processed - Winner: {match_record['winner']}")
        
    def _save_match_to_db(self, match_record: Dict[str, Any]):
        """Save match record to database"""
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO match_history 
            (match_id, start_time, end_time, duration, team_a_score, team_b_score, 
             winner, cheaters_detected, total_events, network_issues)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (match_record['match_id'], match_record['start_time'], match_record['end_time'],
             match_record['duration'], match_record['team_a_score'], match_record['team_b_score'],
             match_record['winner'], match_record['cheaters_detected'], 
             match_record['total_events'], match_record['network_issues']))
        self.conn.commit()
        
    def _update_player_rankings(self, match_data: Dict[str, Any]):
        """Update player rankings based on match results"""
        # This would be populated from agent data
        # For now, simulate player performance
        for i in range(10):  # 10 players
            player_id = f"Player_{i+1}"
            stats = self.player_rankings[player_id]
            
            # Simulate performance
            stats['total_matches'] += 1
            stats['kills'] += np.random.randint(0, 10)
            stats['deaths'] += np.random.randint(0, 8)
            stats['accuracy'] = np.random.uniform(0.3, 0.9)
            stats['avg_score'] = (stats['avg_score'] * (stats['total_matches'] - 1) + 
                                np.random.randint(50, 200)) / stats['total_matches']
            
            # Update database
            self._save_player_stats(player_id, stats)
            
    def _save_player_stats(self, player_id: str, stats: Dict[str, Any]):
        """Save player statistics to database"""
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO player_stats 
            (player_id, total_matches, wins, kills, deaths, accuracy, avg_score, 
             cheat_detections, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (player_id, stats['total_matches'], stats['wins'], stats['kills'],
             stats['deaths'], stats['accuracy'], stats['avg_score'],
             stats['cheat_detections'], datetime.now().isoformat()))
        self.conn.commit()
        
    def update_performance_metrics(self, metrics: Dict[str, float]):
        """Update performance metrics"""
        timestamp = datetime.now().isoformat()
        
        # Store in memory
        self.performance_metrics['network_health'].append(metrics.get('network_health', 1.0))
        self.performance_metrics['fps_history'].append(metrics.get('fps', 60.0))
        self.performance_metrics['cpu_usage'].append(metrics.get('cpu_usage', 0.0))
        self.performance_metrics['memory_usage'].append(metrics.get('memory_usage', 0.0))
        
        # Keep only recent history
        for key in self.performance_metrics:
            if len(self.performance_metrics[key]) > 1000:
                self.performance_metrics[key] = self.performance_metrics[key][-1000:]
        
        # Save to database
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO performance_metrics 
            (timestamp, network_health, fps, cpu_usage, memory_usage)
            VALUES (?, ?, ?, ?, ?)''',
            (timestamp, metrics.get('network_health', 1.0), metrics.get('fps', 60.0),
             metrics.get('cpu_usage', 0.0), metrics.get('memory_usage', 0.0)))
        self.conn.commit()
        
    def get_player_rankings(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top player rankings"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM player_stats 
            ORDER BY avg_score DESC, wins DESC 
            LIMIT ?''', (limit,))
        
        rankings = []
        for row in cursor.fetchall():
            rankings.append({
                'player_id': row[0],
                'total_matches': row[1],
                'wins': row[2],
                'kills': row[3],
                'deaths': row[4],
                'accuracy': row[5],
                'avg_score': row[6],
                'cheat_detections': row[7],
                'kd_ratio': row[3] / max(row[4], 1)  # Avoid division by zero
            })
        
        return rankings
        
    def get_match_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent match history"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM match_history 
            ORDER BY end_time DESC 
            LIMIT ?''', (limit,))
        
        matches = []
        for row in cursor.fetchall():
            matches.append({
                'match_id': row[0],
                'start_time': row[1],
                'end_time': row[2],
                'duration': row[3],
                'team_a_score': row[4],
                'team_b_score': row[5],
                'winner': row[6],
                'cheaters_detected': row[7],
                'total_events': row[8],
                'network_issues': row[9]
            })
        
        return matches
        
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary"""
        if not self.performance_metrics['network_health']:
            return {}
            
        return {
            'network_health': {
                'current': self.performance_metrics['network_health'][-1],
                'average': np.mean(self.performance_metrics['network_health']),
                'min': np.min(self.performance_metrics['network_health']),
                'max': np.max(self.performance_metrics['network_health'])
            },
            'fps': {
                'current': self.performance_metrics['fps_history'][-1],
                'average': np.mean(self.performance_metrics['fps_history']),
                'min': np.min(self.performance_metrics['fps_history']),
                'max': np.max(self.performance_metrics['fps_history'])
            },
            'cpu_usage': {
                'current': self.performance_metrics['cpu_usage'][-1],
                'average': np.mean(self.performance_metrics['cpu_usage'])
            },
            'memory_usage': {
                'current': self.performance_metrics['memory_usage'][-1],
                'average': np.mean(self.performance_metrics['memory_usage'])
            }
        }
        
    def generate_heatmap_data(self) -> Dict[str, Any]:
        """Generate heatmap data for visualization"""
        # Simulate player position heatmap
        heatmap_data = {
            'x': np.random.uniform(-100, 100, 1000).tolist(),
            'y': np.random.uniform(-100, 100, 1000).tolist(),
            'intensity': np.random.uniform(0, 1, 1000).tolist()
        }
        
        return heatmap_data
        
    def get_cheat_analysis(self) -> Dict[str, Any]:
        """Get cheat detection analysis"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT COUNT(*) as total_matches, 
            SUM(cheaters_detected) as total_cheaters 
            FROM match_history''')
        
        row = cursor.fetchone()
        total_matches = row[0] or 0
        total_cheaters = row[1] or 0
        
        return {
            'total_matches': total_matches,
            'total_cheaters_detected': total_cheaters,
            'cheat_rate': total_cheaters / max(total_matches, 1),
            'detection_rate': 0.85,  # Simulated detection rate
            'false_positive_rate': 0.05  # Simulated false positive rate
        }
        
    def export_data(self, format: str = 'json') -> str:
        """Export analytics data"""
        data = {
            'player_rankings': self.get_player_rankings(),
            'match_history': self.get_match_history(),
            'performance_summary': self.get_performance_summary(),
            'cheat_analysis': self.get_cheat_analysis(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        if format == 'json':
            return json.dumps(data, indent=2)
        elif format == 'csv':
            # Export player rankings and match history as CSV
            import io, csv
            output = io.StringIO()
            writer = csv.writer(output)
            # Player rankings
            writer.writerow(['Player Rankings'])
            writer.writerow(['player_id', 'total_matches', 'wins', 'kills', 'deaths', 'accuracy', 'avg_score', 'cheat_detections', 'kd_ratio'])
            for row in data['player_rankings']:
                writer.writerow([row['player_id'], row['total_matches'], row['wins'], row['kills'], row['deaths'], row['accuracy'], row['avg_score'], row['cheat_detections'], row['kd_ratio']])
            # Match history
            writer.writerow([])
            writer.writerow(['Match History'])
            writer.writerow(['match_id', 'start_time', 'end_time', 'duration', 'team_a_score', 'team_b_score', 'winner', 'cheaters_detected', 'total_events', 'network_issues'])
            for row in data['match_history']:
                writer.writerow([row['match_id'], row['start_time'], row['end_time'], row['duration'], row['team_a_score'], row['team_b_score'], row['winner'], row['cheaters_detected'], row['total_events'], row['network_issues']])
            return output.getvalue()
        else:
            return str(data)
            
    async def shutdown(self):
        """Shutdown advanced analytics"""
        logger.info("🛑 Shutting down Advanced Analytics...")
        if self.conn:
            self.conn.close() 