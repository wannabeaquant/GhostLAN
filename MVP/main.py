#!/usr/bin/env python3
"""
GhostLAN SimWorld - Main Application
Advanced eSports Anti-Cheat Testing Platform with Duality AI Integration
Powered by Duality AI - Intelligent Digital Twin Simulation
"""

import asyncio
import logging
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
import os
from typing import Dict, Any, List
from datetime import datetime

# Import all modules
from duality_scene.simulation import SimulationManager
from ghostlan_core.anticheat import AntiCheatEngine
from analytics.pipeline import AnalyticsPipeline
from analytics.match_recorder import MatchRecorder
from api.server import start_api_server
from api.config import config_router
from api.export import export_router
from api.replay import replay_router
from api.tournament import tournament_router
from api.mobile_endpoints import mobile_router
from api.cloud_endpoints import cloud_router
from api.streaming_endpoints import streaming_router

# Import advanced modules (no ML)
from streaming.real_time_streaming import RealTimeStreamingSystem
from mobile.mobile_app import MobileAppBackend
from cloud_integration.cloud_services import CloudIntegrationManager
from advanced_tournament.advanced_tournament import AdvancedTournamentManager

# Import Duality AI configuration
from duality_ai_config import setup_duality_ai, get_duality_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
duality_simulation = None
anticheat_engine = None
analytics_pipeline = None
match_recorder = None
tournament_manager = None
mobile_backend = None
cloud_manager = None
streaming_system = None
advanced_tournament_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global duality_simulation, anticheat_engine, analytics_pipeline
    global match_recorder, tournament_manager, mobile_backend
    global cloud_manager, streaming_system, advanced_tournament_manager
    
    logger.info("🚀 Starting GhostLAN SimWorld - Powered by Duality AI...")
    
    # Setup Duality AI configuration
    duality_ai_enabled = setup_duality_ai()
    
    try:
        # Initialize Duality AI simulation
        if duality_ai_enabled:
            logger.info("🤖 Initializing Duality AI Simulation Environment (API Mode)...")
        else:
            logger.info("🤖 Initializing Duality AI Simulation Environment (Local Mode)...")
        
        duality_simulation = SimulationManager()
        await duality_simulation.initialize()
        logger.info("✅ Duality AI Simulation initialized with 10 intelligent agents")
        
        # Initialize anti-cheat engine
        logger.info("🛡️ Initializing Anti-Cheat Engine...")
        anticheat_engine = AntiCheatEngine()
        await anticheat_engine.initialize()
        
        # Initialize analytics pipeline
        logger.info("📊 Initializing Analytics Pipeline...")
        analytics_pipeline = AnalyticsPipeline()
        await analytics_pipeline.initialize()
        
        # Initialize match recorder
        logger.info("🎬 Initializing Match Recorder...")
        match_recorder = MatchRecorder()
        await match_recorder.initialize()
        
        # Initialize tournament manager
        logger.info("🏆 Initializing Tournament Manager...")
        tournament_manager = AdvancedTournamentManager()
        
        # Initialize mobile app backend
        logger.info("📱 Initializing Mobile App Backend...")
        secret_key = os.getenv("JWT_SECRET_KEY", "ghostlan-secret-key")
        mobile_backend = MobileAppBackend(secret_key, match_recorder, tournament_manager, analytics_pipeline)
        
        # Initialize cloud integration manager
        logger.info("☁️ Initializing Cloud Integration Manager...")
        cloud_manager = CloudIntegrationManager()
        
        # Initialize real-time streaming system
        logger.info("📡 Initializing Real-time Streaming System...")
        streaming_system = RealTimeStreamingSystem()
        
        # Initialize advanced tournament manager
        logger.info("🏆 Initializing Advanced Tournament Manager...")
        advanced_tournament_manager = AdvancedTournamentManager()
        
        logger.info("✅ All systems initialized successfully!")
        logger.info("🎯 Duality AI agents are now running in the digital twin environment")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize systems: {e}")
        raise
    finally:
        # Cleanup
        logger.info("🛑 Shutting down GhostLAN SimWorld...")
        
        if duality_simulation:
            await duality_simulation.shutdown()
        if anticheat_engine:
            await anticheat_engine.shutdown()
        if analytics_pipeline:
            await analytics_pipeline.shutdown()
        if match_recorder:
            await match_recorder.shutdown()
        if mobile_backend:
            await mobile_backend.shutdown()
        if cloud_manager:
            await cloud_manager.shutdown()
        if streaming_system:
            await streaming_system.shutdown()
        if advanced_tournament_manager:
            await advanced_tournament_manager.shutdown()
            
        logger.info("✅ Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="GhostLAN SimWorld - Powered by Duality AI",
    description="Advanced eSports Anti-Cheat Testing Platform with Duality AI Integration - Intelligent Digital Twin Simulation for LAN Tournaments",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers (no ML router)
app.include_router(config_router, prefix="/api/v1")
app.include_router(export_router, prefix="/api/v1")
app.include_router(replay_router, prefix="/api/v1")
app.include_router(tournament_router, prefix="/api/v1")
app.include_router(mobile_router, prefix="/api/v1")
app.include_router(cloud_router, prefix="/api/v1")
app.include_router(streaming_router, prefix="/api/v1")

# WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back with Duality AI branding
            await websocket.send_text(json.dumps({
                "message": "Duality AI Simulation Active",
                "data": data,
                "timestamp": datetime.now().isoformat()
            }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    """Root endpoint with Duality AI branding"""
    duality_config = get_duality_config()
    
    return {
        "message": "GhostLAN SimWorld - Powered by Duality AI",
        "description": "Advanced eSports Anti-Cheat Testing Platform with Duality AI Integration",
        "duality_ai_status": {
            "enabled": duality_config.is_configured(),
            "mode": "API" if duality_config.is_configured() else "Local Simulation"
        },
        "features": {
            "duality_ai_simulation": "Intelligent AI agents in digital twin environment",
            "anti_cheat_testing": "Pre-tournament anti-cheat validation",
            "offline_analytics": "Comprehensive performance analysis",
            "tournament_management": "Complete tournament platform",
            "mobile_integration": "iOS/Android app support",
            "real_time_streaming": "Live tournament broadcasting"
        },
        "duality_ai_agents": {
            "total_agents": 10,
            "normal_agents": 6,
            "cheat_agents": 4,
            "environment": "Realistic LAN café digital twin"
        },
        "version": "2.0.0",
        "powered_by": "Duality AI"
    }

@app.get("/health")
async def health_check():
    """Health check with Duality AI status"""
    duality_config = get_duality_config()
    
    return {
        "status": "healthy",
        "powered_by": "Duality AI",
        "duality_ai": {
            "enabled": duality_config.is_configured(),
            "mode": "API" if duality_config.is_configured() else "Local Simulation",
            "api_url": duality_config.get_api_url() if duality_config.is_configured() else None
        },
        "services": {
            "duality_ai_simulation": duality_simulation is not None,
            "anticheat_engine": anticheat_engine is not None,
            "analytics_pipeline": analytics_pipeline is not None,
            "match_recorder": match_recorder is not None,
            "tournament_manager": tournament_manager is not None,
            "mobile_backend": mobile_backend is not None,
            "cloud_manager": cloud_manager is not None,
            "streaming_system": streaming_system is not None,
            "advanced_tournament_manager": advanced_tournament_manager is not None
        },
        "duality_ai_status": {
            "agents_running": duality_simulation is not None,
            "environment_active": duality_simulation is not None,
            "simulation_healthy": duality_simulation is not None
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/v1/status")
async def api_status():
    """API status with Duality AI integration details"""
    duality_config = get_duality_config()
    
    return {
        "api_version": "v1",
        "status": "operational",
        "powered_by": "Duality AI",
        "duality_ai": {
            "enabled": duality_config.is_configured(),
            "mode": "API" if duality_config.is_configured() else "Local Simulation"
        },
        "features": {
            "config_management": True,
            "data_export": True,
            "match_replay": True,
            "tournament_management": True,
            "mobile_api": True,
            "cloud_integration": True,
            "streaming": True
        },
        "duality_ai_integration": {
            "simulation_active": True,
            "agents_count": 10,
            "environment_type": "LAN café digital twin",
            "ai_capabilities": [
                "Intelligent gameplay simulation",
                "Configurable cheating behavior",
                "Realistic player behavior",
                "Dynamic environment interaction"
            ]
        },
        "endpoints": {
            "config": "/api/v1/config",
            "export": "/api/v1/export",
            "replay": "/api/v1/replay",
            "tournament": "/api/v1/tournament",
            "mobile": "/api/v1/mobile",
            "cloud": "/api/v1/cloud",
            "streaming": "/api/v1/streaming"
        }
    }

# Helper functions
def get_duality_simulation():
    return duality_simulation

def get_anticheat_engine():
    return anticheat_engine

def get_analytics_pipeline():
    return analytics_pipeline

def get_match_recorder():
    return match_recorder

def get_tournament_manager():
    return tournament_manager

def get_mobile_backend():
    return mobile_backend

def get_cloud_manager():
    return cloud_manager

def get_streaming_system():
    return streaming_system

def get_advanced_tournament_manager():
    return advanced_tournament_manager

# Store instances in app state
@app.on_event("startup")
async def startup_event():
    app.state.duality_simulation = duality_simulation
    app.state.anticheat_engine = anticheat_engine
    app.state.analytics_pipeline = analytics_pipeline
    app.state.match_recorder = match_recorder
    app.state.tournament_manager = tournament_manager
    app.state.mobile_backend = mobile_backend
    app.state.cloud_manager = cloud_manager
    app.state.streaming_system = streaming_system
    app.state.advanced_tournament_manager = advanced_tournament_manager

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 