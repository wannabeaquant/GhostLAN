"""
Config API for GhostLAN SimWorld
Endpoints for getting/setting simulation parameters
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

config_router = APIRouter()

# In-memory config (should be replaced with persistent storage in production)
simulation_config = {
    'num_players': 10,
    'cheat_probability': 0.3,
    'match_duration': 300,
    'tick_rate': 60.0,
    'network_conditions': {
        'packet_loss': 0.02,
        'latency': 15.0,
        'jitter': 5.0,
        'bandwidth': 100.0
    }
}

class ConfigUpdate(BaseModel):
    num_players: int = 10
    cheat_probability: float = 0.3
    match_duration: int = 300
    tick_rate: float = 60.0
    network_conditions: dict = simulation_config['network_conditions']

@config_router.get("/config")
def get_config():
    return simulation_config

@config_router.post("/config")
def update_config(update: ConfigUpdate):
    simulation_config.update(update.dict())
    return {"status": "ok", "config": simulation_config} 