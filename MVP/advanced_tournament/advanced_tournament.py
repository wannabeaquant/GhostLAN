"""
Advanced Tournament System for GhostLAN SimWorld
Double elimination, Swiss system, round-robin, and prize distribution
"""

import asyncio
import logging
import json
import random
import math
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import heapq

logger = logging.getLogger(__name__)

class TournamentType(Enum):
    """Tournament types"""
    SINGLE_ELIMINATION = "single_elimination"
    DOUBLE_ELIMINATION = "double_elimination"
    SWISS_SYSTEM = "swiss_system"
    ROUND_ROBIN = "round_robin"
    BRACKET = "bracket"

class MatchStatus(Enum):
    """Match status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class TournamentParticipant:
    """Tournament participant"""
    user_id: str
    username: str
    seed: int
    rating: float
    wins: int = 0
    losses: int = 0
    draws: int = 0
    points: int = 0
    eliminated: bool = False
    eliminated_round: Optional[int] = None

@dataclass
class TournamentMatch:
    """Tournament match"""
    match_id: str
    tournament_id: str
    round_number: int
    match_number: int
    player1_id: str
    player2_id: Optional[str] = None
    winner_id: Optional[str] = None
    loser_id: Optional[str] = None
    status: MatchStatus = MatchStatus.PENDING
    score: Optional[Dict[str, int]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

@dataclass
class PrizePool:
    """Tournament prize pool"""
    total_amount: float
    currency: str = "USD"
    distribution: Dict[int, float] = None  # position -> percentage
    
    def __post_init__(self):
        if self.distribution is None:
            # Default distribution: 1st=50%, 2nd=30%, 3rd=20%
            self.distribution = {1: 0.50, 2: 0.30, 3: 0.20}

class DoubleEliminationBracket:
    """Double elimination tournament bracket"""
    
    def __init__(self, participants: List[TournamentParticipant]):
        self.participants = participants
        self.winners_bracket = []
        self.losers_bracket = []
        self.final_matches = []
        self.current_round = 0
        
    def generate_bracket(self) -> Dict[str, Any]:
        """Generate double elimination bracket"""
        # Winners bracket (single elimination)
        self.winners_bracket = self._generate_single_elimination_bracket()
        
        # Losers bracket (double elimination)
        self.losers_bracket = self._generate_losers_bracket()
        
        # Final matches
        self.final_matches = self._generate_final_matches()
        
        return {
            'winners_bracket': self.winners_bracket,
            'losers_bracket': self.losers_bracket,
            'final_matches': self.final_matches
        }
        
    def _generate_single_elimination_bracket(self) -> List[List[Dict[str, Any]]]:
        """Generate single elimination bracket"""
        num_players = len(self.participants)
        rounds = math.ceil(math.log2(num_players))
        
        bracket = []
        for round_num in range(rounds):
            round_matches = []
            matches_in_round = 2 ** (rounds - round_num - 1)
            
            for match_num in range(matches_in_round):
                match = {
                    'round': round_num + 1,
                    'match_number': match_num + 1,
                    'player1': None,
                    'player2': None,
                    'winner': None,
                    'next_match': match_num // 2 + 1
                }
                round_matches.append(match)
                
            bracket.append(round_matches)
            
        # Seed players
        self._seed_players(bracket)
        return bracket
        
    def _generate_losers_bracket(self) -> List[List[Dict[str, Any]]]:
        """Generate losers bracket"""
        num_players = len(self.participants)
        rounds = math.ceil(math.log2(num_players)) * 2 - 1
        
        bracket = []
        for round_num in range(rounds):
            round_matches = []
            matches_in_round = max(1, num_players // (2 ** (round_num + 1)))
            
            for match_num in range(matches_in_round):
                match = {
                    'round': round_num + 1,
                    'match_number': match_num + 1,
                    'player1': None,
                    'player2': None,
                    'winner': None,
                    'next_match': match_num // 2 + 1
                }
                round_matches.append(match)
                
            bracket.append(round_matches)
            
        return bracket
        
    def _generate_final_matches(self) -> List[Dict[str, Any]]:
        """Generate final matches"""
        return [
            {
                'round': 'final',
                'match_number': 1,
                'player1': None,  # Winner of winners bracket
                'player2': None,  # Winner of losers bracket
                'winner': None,
                'reset_match': False
            },
            {
                'round': 'final_reset',
                'match_number': 2,
                'player1': None,  # Winner of first final
                'player2': None,  # Loser of first final
                'winner': None,
                'reset_match': True
            }
        ]
        
    def _seed_players(self, bracket: List[List[Dict[str, Any]]]):
        """Seed players into bracket"""
        # Simple seeding - in production would use more sophisticated seeding
        for i, participant in enumerate(self.participants):
            if i < len(bracket[0]):
                bracket[0][i]['player1'] = participant.user_id

class SwissSystemTournament:
    """Swiss system tournament"""
    
    def __init__(self, participants: List[TournamentParticipant], rounds: int = 5):
        self.participants = participants
        self.rounds = rounds
        self.current_round = 0
        self.matches = []
        self.standings = []
        
    def generate_pairings(self, round_number: int) -> List[Dict[str, Any]]:
        """Generate pairings for Swiss system round"""
        if round_number == 1:
            # First round: random pairings
            return self._random_pairings()
        else:
            # Subsequent rounds: pair by score
            return self._score_based_pairings()
            
    def _random_pairings(self) -> List[Dict[str, Any]]:
        """Generate random pairings for first round"""
        shuffled = self.participants.copy()
        random.shuffle(shuffled)
        
        pairings = []
        for i in range(0, len(shuffled), 2):
            if i + 1 < len(shuffled):
                pairing = {
                    'round': 1,
                    'match_number': i // 2 + 1,
                    'player1': shuffled[i].user_id,
                    'player2': shuffled[i + 1].user_id,
                    'player1_score': shuffled[i].points,
                    'player2_score': shuffled[i + 1].points
                }
                pairings.append(pairing)
            else:
                # Bye for odd player
                pairing = {
                    'round': 1,
                    'match_number': i // 2 + 1,
                    'player1': shuffled[i].user_id,
                    'player2': None,
                    'player1_score': shuffled[i].points,
                    'player2_score': 0
                }
                pairings.append(pairing)
                
        return pairings
        
    def _score_based_pairings(self) -> List[Dict[str, Any]]:
        """Generate score-based pairings"""
        # Sort by points (descending)
        sorted_participants = sorted(self.participants, key=lambda p: p.points, reverse=True)
        
        pairings = []
        used = set()
        
        for i, player1 in enumerate(sorted_participants):
            if player1.user_id in used:
                continue
                
            # Find best available opponent
            best_opponent = None
            best_score_diff = float('inf')
            
            for j, player2 in enumerate(sorted_participants[i + 1:], i + 1):
                if player2.user_id in used:
                    continue
                    
                # Check if they haven't played before
                if not self._have_played_before(player1.user_id, player2.user_id):
                    score_diff = abs(player1.points - player2.points)
                    if score_diff < best_score_diff:
                        best_score_diff = score_diff
                        best_opponent = player2
                        
            if best_opponent:
                pairing = {
                    'round': self.current_round + 1,
                    'match_number': len(pairings) + 1,
                    'player1': player1.user_id,
                    'player2': best_opponent.user_id,
                    'player1_score': player1.points,
                    'player2_score': best_opponent.points
                }
                pairings.append(pairing)
                used.add(player1.user_id)
                used.add(best_opponent.user_id)
            else:
                # Bye for unmatched player
                pairing = {
                    'round': self.current_round + 1,
                    'match_number': len(pairings) + 1,
                    'player1': player1.user_id,
                    'player2': None,
                    'player1_score': player1.points,
                    'player2_score': 0
                }
                pairings.append(pairing)
                used.add(player1.user_id)
                
        return pairings
        
    def _have_played_before(self, player1_id: str, player2_id: str) -> bool:
        """Check if two players have played before"""
        for match in self.matches:
            if ((match['player1'] == player1_id and match['player2'] == player2_id) or
                (match['player1'] == player2_id and match['player2'] == player1_id)):
                return True
        return False
        
    def update_standings(self):
        """Update tournament standings"""
        self.standings = sorted(self.participants, key=lambda p: (p.points, p.rating), reverse=True)
        
    def get_final_standings(self) -> List[Dict[str, Any]]:
        """Get final tournament standings"""
        self.update_standings()
        return [
            {
                'position': i + 1,
                'user_id': participant.user_id,
                'username': participant.username,
                'points': participant.points,
                'wins': participant.wins,
                'losses': participant.losses,
                'draws': participant.draws,
                'rating': participant.rating
            }
            for i, participant in enumerate(self.standings)
        ]

class RoundRobinTournament:
    """Round-robin tournament"""
    
    def __init__(self, participants: List[TournamentParticipant]):
        self.participants = participants
        self.matches = []
        self.standings = []
        
    def generate_schedule(self) -> List[Dict[str, Any]]:
        """Generate round-robin schedule"""
        num_players = len(self.participants)
        
        if num_players % 2 == 1:
            # Add bye player for odd number
            bye_player = TournamentParticipant(
                user_id="bye",
                username="BYE",
                seed=num_players + 1,
                rating=0
            )
            self.participants.append(bye_player)
            num_players += 1
            
        rounds = num_players - 1
        matches_per_round = num_players // 2
        
        schedule = []
        for round_num in range(rounds):
            round_matches = []
            for match_num in range(matches_per_round):
                player1_idx = (round_num + match_num) % (num_players - 1)
                player2_idx = (num_players - 1 - match_num + round_num) % (num_players - 1)
                
                if match_num == 0:
                    player2_idx = num_players - 1
                    
                match = {
                    'round': round_num + 1,
                    'match_number': match_num + 1,
                    'player1': self.participants[player1_idx].user_id,
                    'player2': self.participants[player2_idx].user_id,
                    'player1_name': self.participants[player1_idx].username,
                    'player2_name': self.participants[player2_idx].username
                }
                round_matches.append(match)
                
            schedule.append(round_matches)
            
        return schedule

class PrizeDistribution:
    """Prize distribution system"""
    
    def __init__(self, prize_pool: PrizePool):
        self.prize_pool = prize_pool
        
    def calculate_prizes(self, standings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate prize distribution"""
        prizes = []
        
        for standing in standings:
            position = standing['position']
            if position in self.prize_pool.distribution:
                amount = self.prize_pool.total_amount * self.prize_pool.distribution[position]
                prize = {
                    'position': position,
                    'user_id': standing['user_id'],
                    'username': standing['username'],
                    'amount': amount,
                    'currency': self.prize_pool.currency,
                    'percentage': self.prize_pool.distribution[position] * 100
                }
                prizes.append(prize)
                
        return prizes
        
    def generate_payout_report(self, prizes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate payout report"""
        total_paid = sum(prize['amount'] for prize in prizes)
        
        return {
            'total_prize_pool': self.prize_pool.total_amount,
            'total_paid': total_paid,
            'currency': self.prize_pool.currency,
            'prizes': prizes,
            'distribution_summary': {
                position: {
                    'amount': self.prize_pool.total_amount * percentage,
                    'percentage': percentage * 100
                }
                for position, percentage in self.prize_pool.distribution.items()
            }
        }

class AdvancedTournamentManager:
    """Advanced tournament management system"""
    
    def __init__(self):
        self.tournaments = {}
        self.participants = {}
        self.matches = {}
        self.brackets = {}
        self.prize_pools = {}
        
    async def create_tournament(self, tournament_id: str, name: str, 
                              tournament_type: TournamentType, 
                              participants: List[Dict[str, Any]],
                              prize_pool: Optional[PrizePool] = None,
                              **kwargs) -> Dict[str, Any]:
        """Create advanced tournament"""
        
        # Create tournament participants
        tournament_participants = []
        for i, participant_data in enumerate(participants):
            participant = TournamentParticipant(
                user_id=participant_data['user_id'],
                username=participant_data['username'],
                seed=i + 1,
                rating=participant_data.get('rating', 1000.0)
            )
            tournament_participants.append(participant)
            
        # Store tournament data
        tournament = {
            'tournament_id': tournament_id,
            'name': name,
            'type': tournament_type.value,
            'participants': tournament_participants,
            'status': 'created',
            'created_at': datetime.utcnow(),
            'start_date': kwargs.get('start_date'),
            'end_date': kwargs.get('end_date'),
            'current_round': 0,
            'total_rounds': kwargs.get('total_rounds', 1),
            'settings': kwargs.get('settings', {})
        }
        
        self.tournaments[tournament_id] = tournament
        self.participants[tournament_id] = tournament_participants
        
        # Set up tournament structure based on type
        if tournament_type == TournamentType.DOUBLE_ELIMINATION:
            bracket = DoubleEliminationBracket(tournament_participants)
            bracket_data = bracket.generate_bracket()
            self.brackets[tournament_id] = bracket_data
            
        elif tournament_type == TournamentType.SWISS_SYSTEM:
            swiss = SwissSystemTournament(tournament_participants, kwargs.get('rounds', 5))
            self.brackets[tournament_id] = {'type': 'swiss', 'tournament': swiss}
            
        elif tournament_type == TournamentType.ROUND_ROBIN:
            round_robin = RoundRobinTournament(tournament_participants)
            schedule = round_robin.generate_schedule()
            self.brackets[tournament_id] = {'type': 'round_robin', 'schedule': schedule}
            
        # Set up prize pool
        if prize_pool:
            self.prize_pools[tournament_id] = prize_pool
            
        logger.info(f"🏆 Advanced tournament created: {name} ({tournament_type.value})")
        return tournament
        
    async def start_tournament(self, tournament_id: str) -> Dict[str, Any]:
        """Start tournament"""
        if tournament_id not in self.tournaments:
            return {'success': False, 'error': 'Tournament not found'}
            
        tournament = self.tournaments[tournament_id]
        tournament['status'] = 'in_progress'
        tournament['started_at'] = datetime.utcnow()
        
        # Generate first round matches
        await self._generate_next_round(tournament_id)
        
        logger.info(f"🏆 Tournament started: {tournament['name']}")
        return {'success': True, 'tournament': tournament}
        
    async def _generate_next_round(self, tournament_id: str):
        """Generate next round matches"""
        tournament = self.tournaments[tournament_id]
        tournament_type = TournamentType(tournament['type'])
        
        if tournament_type == TournamentType.DOUBLE_ELIMINATION:
            await self._generate_double_elimination_round(tournament_id)
        elif tournament_type == TournamentType.SWISS_SYSTEM:
            await self._generate_swiss_round(tournament_id)
        elif tournament_type == TournamentType.ROUND_ROBIN:
            await self._generate_round_robin_round(tournament_id)
            
    async def _generate_double_elimination_round(self, tournament_id: str):
        """Generate double elimination round"""
        bracket = self.brackets[tournament_id]
        current_round = self.tournaments[tournament_id]['current_round']
        
        # Generate matches for current round
        matches = []
        if current_round == 0:
            # First round - winners bracket
            for match in bracket['winners_bracket'][0]:
                tournament_match = TournamentMatch(
                    match_id=f"{tournament_id}_w{current_round}_{match['match_number']}",
                    tournament_id=tournament_id,
                    round_number=current_round + 1,
                    match_number=match['match_number'],
                    player1_id=match['player1'],
                    player2_id=match['player2']
                )
                matches.append(tournament_match)
                
        self.matches[tournament_id] = matches
        
    async def _generate_swiss_round(self, tournament_id: str):
        """Generate Swiss system round"""
        bracket = self.brackets[tournament_id]
        swiss_tournament = bracket['tournament']
        
        pairings = swiss_tournament.generate_pairings(swiss_tournament.current_round + 1)
        
        matches = []
        for pairing in pairings:
            tournament_match = TournamentMatch(
                match_id=f"{tournament_id}_s{pairing['round']}_{pairing['match_number']}",
                tournament_id=tournament_id,
                round_number=pairing['round'],
                match_number=pairing['match_number'],
                player1_id=pairing['player1'],
                player2_id=pairing['player2']
            )
            matches.append(tournament_match)
            
        self.matches[tournament_id] = matches
        
    async def _generate_round_robin_round(self, tournament_id: str):
        """Generate round-robin round"""
        bracket = self.brackets[tournament_id]
        schedule = bracket['schedule']
        current_round = self.tournaments[tournament_id]['current_round']
        
        if current_round < len(schedule):
            round_matches = schedule[current_round]
            matches = []
            
            for match in round_matches:
                tournament_match = TournamentMatch(
                    match_id=f"{tournament_id}_rr{current_round + 1}_{match['match_number']}",
                    tournament_id=tournament_id,
                    round_number=current_round + 1,
                    match_number=match['match_number'],
                    player1_id=match['player1'],
                    player2_id=match['player2']
                )
                matches.append(tournament_match)
                
            self.matches[tournament_id] = matches
            
    async def record_match_result(self, tournament_id: str, match_id: str, 
                                winner_id: str, loser_id: str, score: Dict[str, int]) -> Dict[str, Any]:
        """Record match result"""
        if tournament_id not in self.matches:
            return {'success': False, 'error': 'Tournament not found'}
            
        # Find and update match
        for match in self.matches[tournament_id]:
            if match.match_id == match_id:
                match.winner_id = winner_id
                match.loser_id = loser_id
                match.score = score
                match.status = MatchStatus.COMPLETED
                match.end_time = datetime.utcnow()
                break
                
        # Update participant records
        await self._update_participant_records(tournament_id, winner_id, loser_id)
        
        # Check if round is complete
        if await self._is_round_complete(tournament_id):
            await self._advance_tournament(tournament_id)
            
        return {'success': True}
        
    async def _update_participant_records(self, tournament_id: str, winner_id: str, loser_id: str):
        """Update participant win/loss records"""
        participants = self.participants[tournament_id]
        
        for participant in participants:
            if participant.user_id == winner_id:
                participant.wins += 1
                participant.points += 3
            elif participant.user_id == loser_id:
                participant.losses += 1
                
    async def _is_round_complete(self, tournament_id: str) -> bool:
        """Check if current round is complete"""
        matches = self.matches.get(tournament_id, [])
        return all(match.status == MatchStatus.COMPLETED for match in matches)
        
    async def _advance_tournament(self, tournament_id: str):
        """Advance tournament to next round"""
        tournament = self.tournaments[tournament_id]
        tournament['current_round'] += 1
        
        # Check if tournament is complete
        if await self._is_tournament_complete(tournament_id):
            await self._complete_tournament(tournament_id)
        else:
            # Generate next round
            await self._generate_next_round(tournament_id)
            
    async def _is_tournament_complete(self, tournament_id: str) -> bool:
        """Check if tournament is complete"""
        tournament = self.tournaments[tournament_id]
        tournament_type = TournamentType(tournament['type'])
        
        if tournament_type == TournamentType.DOUBLE_ELIMINATION:
            # Check if final match is complete
            return False  # Simplified
        elif tournament_type == TournamentType.SWISS_SYSTEM:
            return tournament['current_round'] >= tournament['total_rounds']
        elif tournament_type == TournamentType.ROUND_ROBIN:
            bracket = self.brackets[tournament_id]
            return tournament['current_round'] >= len(bracket['schedule'])
            
        return False
        
    async def _complete_tournament(self, tournament_id: str):
        """Complete tournament and calculate final standings"""
        tournament = self.tournaments[tournament_id]
        tournament['status'] = 'completed'
        tournament['completed_at'] = datetime.utcnow()
        
        # Calculate final standings
        standings = await self._calculate_final_standings(tournament_id)
        tournament['final_standings'] = standings
        
        # Calculate prizes if applicable
        if tournament_id in self.prize_pools:
            prize_distribution = PrizeDistribution(self.prize_pools[tournament_id])
            prizes = prize_distribution.calculate_prizes(standings)
            tournament['prizes'] = prizes
            
        logger.info(f"🏆 Tournament completed: {tournament['name']}")
        
    async def _calculate_final_standings(self, tournament_id: str) -> List[Dict[str, Any]]:
        """Calculate final tournament standings"""
        participants = self.participants[tournament_id]
        tournament = self.tournaments[tournament_id]
        tournament_type = TournamentType(tournament['type'])
        
        if tournament_type == TournamentType.SWISS_SYSTEM:
            bracket = self.brackets[tournament_id]
            swiss_tournament = bracket['tournament']
            return swiss_tournament.get_final_standings()
        else:
            # Sort by points, then by wins, then by rating
            sorted_participants = sorted(
                participants,
                key=lambda p: (p.points, p.wins, p.rating),
                reverse=True
            )
            
            return [
                {
                    'position': i + 1,
                    'user_id': participant.user_id,
                    'username': participant.username,
                    'points': participant.points,
                    'wins': participant.wins,
                    'losses': participant.losses,
                    'draws': participant.draws,
                    'rating': participant.rating
                }
                for i, participant in enumerate(sorted_participants)
            ]
            
    async def get_tournament_info(self, tournament_id: str) -> Dict[str, Any]:
        """Get tournament information"""
        if tournament_id not in self.tournaments:
            return {'error': 'Tournament not found'}
            
        tournament = self.tournaments[tournament_id]
        return {
            'tournament': tournament,
            'bracket': self.brackets.get(tournament_id),
            'matches': [asdict(match) for match in self.matches.get(tournament_id, [])],
            'participants': [asdict(p) for p in self.participants.get(tournament_id, [])]
        }
        
    async def get_tournaments(self) -> List[Dict[str, Any]]:
        """Get all tournaments"""
        return list(self.tournaments.values())
        
    async def shutdown(self):
        """Shutdown tournament manager"""
        logger.info("🛑 Shutting down Advanced Tournament Manager...") 