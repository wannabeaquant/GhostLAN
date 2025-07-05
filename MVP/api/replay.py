"""
Replay API for GhostLAN SimWorld
Endpoints for match recording and replay
"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, Response
from analytics.match_recorder import MatchRecorder
from typing import List, Dict, Any

replay_router = APIRouter()

match_recorder = MatchRecorder()

@replay_router.get("/replay/matches")
def get_recorded_matches():
    """Get list of recorded matches"""
    return match_recorder.get_recorded_matches()

@replay_router.get("/replay/matches/{match_id}")
def get_match_events(match_id: str):
    """Get events for a specific match"""
    events = match_recorder.load_match_events(match_id)
    summary = match_recorder.get_match_summary(match_id)
    return {
        "match_id": match_id,
        "summary": summary,
        "events": events
    }

@replay_router.get("/replay/matches/{match_id}/export")
def export_match(match_id: str, format: str = Query('json', enum=['json', 'csv'])):
    """Export a match in specified format"""
    data = match_recorder.export_match(match_id, format=format)
    if format == 'json':
        return JSONResponse(content=data)
    elif format == 'csv':
        return Response(content=data, media_type='text/csv')

@replay_router.delete("/replay/matches/{match_id}")
def delete_match(match_id: str):
    """Delete a recorded match"""
    match_recorder.delete_match(match_id)
    return {"status": "deleted"}

@replay_router.post("/replay/start-recording")
def start_recording(match_id: str, config: Dict[str, Any]):
    """Start recording a new match"""
    match_recorder.start_recording(match_id, config)
    return {"status": "recording started"}

@replay_router.post("/replay/stop-recording")
def stop_recording(summary: Dict[str, Any]):
    """Stop recording current match"""
    match_recorder.stop_recording(summary)
    return {"status": "recording stopped"} 