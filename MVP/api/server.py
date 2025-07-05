"""
FastAPI Backend for GhostLAN SimWorld
Exposes endpoints for simulation, anti-cheat, and analytics
"""

import logging
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
from api.config import config_router
from api.tournament import tournament_router
from api.export import export_router
from api.replay import replay_router

logger = logging.getLogger(__name__)

app = FastAPI(title="GhostLAN SimWorld API")

# These will be set by main.py
simulation_manager = None
anticheat_engine = None
analytics_pipeline = None

@app.get("/state")
async def get_simulation_state():
    if simulation_manager:
        return simulation_manager.get_current_state()
    return JSONResponse(status_code=503, content={"error": "Simulation not running"})

@app.get("/detections")
async def get_detections():
    if anticheat_engine:
        return anticheat_engine.get_detections()
    return JSONResponse(status_code=503, content={"error": "Anti-cheat not running"})

@app.get("/analytics")
async def get_analytics():
    if analytics_pipeline:
        return analytics_pipeline.get_latest_analytics()
    return JSONResponse(status_code=503, content={"error": "Analytics not running"})

@app.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    await websocket.accept()
    while True:
        if simulation_manager:
            events = simulation_manager.get_events()
            await websocket.send_json(events[-1] if events else {})
        await asyncio.sleep(0.5)

app.include_router(config_router)
app.include_router(tournament_router)
app.include_router(export_router)
app.include_router(replay_router)

async def start_api_server(anticheat, analytics):
    global simulation_manager, anticheat_engine, analytics_pipeline
    from duality_scene.simulation import SimulationManager
    simulation_manager = SimulationManager()
    anticheat_engine = anticheat
    analytics_pipeline = analytics
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve() 