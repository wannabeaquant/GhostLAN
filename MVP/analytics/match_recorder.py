"""
Match Recording and Replay for GhostLAN SimWorld
Save match events and allow loading/playback
"""

import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import sqlite3

logger = logging.getLogger(__name__)

class MatchRecorder:
    """Records and replays match events"""
    
    def __init__(self, db_path: str = "matches.db"):
        self.db_path = db_path
        self.conn = None
        self.current_match_id = None
        self.recording = False
        
    async def initialize(self):
        """Initialize match recorder"""
        logger.info("🎬 Initializing Match Recorder...")
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()
        
    def _create_tables(self):
        """Create match recording tables"""
        cursor = self.conn.cursor()
        
        # Matches table
        cursor.execute('''CREATE TABLE IF NOT EXISTS matches (
            match_id TEXT PRIMARY KEY,
            start_time TEXT,
            end_time TEXT,
            duration REAL,
            config TEXT,
            summary TEXT
        )''')
        
        # Match events table
        cursor.execute('''CREATE TABLE IF NOT EXISTS match_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id TEXT,
            tick INTEGER,
            event_type TEXT,
            event_data TEXT,
            timestamp TEXT,
            FOREIGN KEY (match_id) REFERENCES matches (match_id)
        )''')
        
        self.conn.commit()
        
    def start_recording(self, match_id: str, config: Dict[str, Any]):
        """Start recording a new match"""
        self.current_match_id = match_id
        self.recording = True
        
        # Save match metadata
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO matches (match_id, start_time, config)
            VALUES (?, ?, ?)''',
            (match_id, datetime.now().isoformat(), json.dumps(config)))
        self.conn.commit()
        
        logger.info(f"🎬 Started recording match {match_id}")
        
    def record_event(self, event: Dict[str, Any]):
        """Record a match event"""
        if not self.recording or not self.current_match_id:
            return
            
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO match_events 
            (match_id, tick, event_type, event_data, timestamp)
            VALUES (?, ?, ?, ?, ?)''',
            (self.current_match_id, 
             event.get('tick', 0),
             event.get('type', 'unknown'),
             json.dumps(event),
             event.get('timestamp', datetime.now().isoformat())))
        self.conn.commit()
        
    def stop_recording(self, summary: Dict[str, Any]):
        """Stop recording and save match summary"""
        if not self.recording or not self.current_match_id:
            return
            
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE matches 
            SET end_time = ?, summary = ?
            WHERE match_id = ?''',
            (datetime.now().isoformat(), json.dumps(summary), self.current_match_id))
        self.conn.commit()
        
        self.recording = False
        self.current_match_id = None
        
        logger.info(f"🎬 Stopped recording match")
        
    def get_recorded_matches(self) -> List[Dict[str, Any]]:
        """Get list of recorded matches"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT match_id, start_time, end_time, duration, summary 
            FROM matches ORDER BY start_time DESC''')
        
        matches = []
        for row in cursor.fetchall():
            matches.append({
                'match_id': row[0],
                'start_time': row[1],
                'end_time': row[2],
                'duration': row[3],
                'summary': json.loads(row[4]) if row[4] else {}
            })
        
        return matches
        
    def load_match_events(self, match_id: str) -> List[Dict[str, Any]]:
        """Load all events for a specific match"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT tick, event_type, event_data, timestamp 
            FROM match_events 
            WHERE match_id = ? 
            ORDER BY tick, timestamp''', (match_id,))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'tick': row[0],
                'type': row[1],
                'data': json.loads(row[2]),
                'timestamp': row[3]
            })
        
        return events
        
    def get_match_summary(self, match_id: str) -> Dict[str, Any]:
        """Get summary for a specific match"""
        cursor = self.conn.cursor()
        cursor.execute('''SELECT summary FROM matches WHERE match_id = ?''', (match_id,))
        
        row = cursor.fetchone()
        if row and row[0]:
            return json.loads(row[0])
        return {}
        
    def delete_match(self, match_id: str):
        """Delete a recorded match"""
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM match_events WHERE match_id = ?''', (match_id,))
        cursor.execute('''DELETE FROM matches WHERE match_id = ?''', (match_id,))
        self.conn.commit()
        
        logger.info(f"🗑️ Deleted match {match_id}")
        
    def export_match(self, match_id: str, format: str = 'json') -> str:
        """Export a match in specified format"""
        events = self.load_match_events(match_id)
        summary = self.get_match_summary(match_id)
        
        match_data = {
            'match_id': match_id,
            'summary': summary,
            'events': events,
            'export_timestamp': datetime.now().isoformat()
        }
        
        if format == 'json':
            return json.dumps(match_data, indent=2)
        elif format == 'csv':
            import io, csv
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write summary
            writer.writerow(['Match Summary'])
            for key, value in summary.items():
                writer.writerow([key, value])
            
            writer.writerow([])
            writer.writerow(['Events'])
            writer.writerow(['tick', 'type', 'timestamp', 'data'])
            
            for event in events:
                writer.writerow([
                    event['tick'],
                    event['type'],
                    event['timestamp'],
                    json.dumps(event['data'])
                ])
            
            return output.getvalue()
        else:
            return str(match_data)
            
    async def shutdown(self):
        """Shutdown match recorder"""
        logger.info("🛑 Shutting down Match Recorder...")
        if self.conn:
            self.conn.close() 