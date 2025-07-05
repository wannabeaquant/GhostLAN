"""
Analytics Pipeline for GhostLAN SimWorld
Logs events, generates synthetic telemetry, and provides analytics
"""

import logging
from typing import List, Dict, Any
import sqlite3
import json
import os
import asyncio

logger = logging.getLogger(__name__)

class AnalyticsPipeline:
    """Analytics pipeline for event logging and telemetry"""
    def __init__(self, db_path: str = "analytics.db"):
        self.db_path = db_path
        self.conn = None
        self.events = []
        self.analytics = {}

    async def initialize(self):
        logger.info("📊 Initializing Analytics Pipeline...")
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tick INTEGER,
            type TEXT,
            data TEXT,
            timestamp TEXT
        )''')
        self.conn.commit()

    async def run(self):
        logger.info("📈 Analytics pipeline running...")
        while True:
            await asyncio.sleep(1)
            self._flush_events()
            self._generate_analytics()

    def log_event(self, event: Dict[str, Any]):
        self.events.append(event)

    def _flush_events(self):
        if not self.events:
            return
        cursor = self.conn.cursor()
        for event in self.events:
            cursor.execute('''INSERT INTO events (tick, type, data, timestamp) VALUES (?, ?, ?, ?)''',
                (event.get('tick'), event.get('type'), json.dumps(event.get('data', {})), str(event.get('timestamp'))))
        self.conn.commit()
        self.events = []

    def _generate_analytics(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT type, COUNT(*) FROM events GROUP BY type''')
        counts = {row[0]: row[1] for row in cursor.fetchall()}
        self.analytics = counts

    def get_latest_analytics(self) -> Dict[str, Any]:
        return self.analytics.copy()

    async def shutdown(self):
        logger.info("🛑 Shutting down Analytics Pipeline...")
        if self.conn:
            self.conn.close() 