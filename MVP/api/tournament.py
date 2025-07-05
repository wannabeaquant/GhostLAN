"""
Tournament API for GhostLAN SimWorld
Endpoints for tournament mode, brackets, and leaderboard
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import random
from pydantic import BaseModel
from advanced_tournament.advanced_tournament import AdvancedTournamentManager

tournament_router = APIRouter()

tournament_state = {
    'started': False,
    'matches': [],
    'leaderboard': []
}

@tournament_router.post("/tournament/start")
def start_tournament():
    # Simulate tournament with 4 teams, 2 rounds
    teams = [f"Team_{i+1}" for i in range(4)]
    matches = [
        {'match_id': 1, 'round': 1, 'team_a': teams[0], 'team_b': teams[1]},
        {'match_id': 2, 'round': 1, 'team_a': teams[2], 'team_b': teams[3]},
        {'match_id': 3, 'round': 2, 'team_a': 'Winner_1', 'team_b': 'Winner_2'}
    ]
    tournament_state['started'] = True
    tournament_state['matches'] = matches
    # Simulate leaderboard
    leaderboard = [
        {'player': f'Player_{i+1}', 'wins': random.randint(0, 3), 'score': random.randint(100, 300)} for i in range(8)
    ]
    tournament_state['leaderboard'] = leaderboard
    return {"status": "tournament started", "matches": matches}

@tournament_router.get("/tournament/bracket")
def get_bracket():
    return {'matches': tournament_state['matches']}

@tournament_router.get("/tournament/leaderboard")
def get_leaderboard():
    return tournament_state['leaderboard'] 