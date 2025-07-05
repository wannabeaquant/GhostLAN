"""
Simulation Manager for GhostLAN SimWorld
Orchestrates Duality AI scene and agent interactions
"""

import asyncio
import logging
import random
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from .environment import LANEnvironment
from .agents import Agent, CheatAgent, NormalAgent

logger = logging.getLogger(__name__)

@dataclass
class SimulationConfig:
    """Configuration for simulation parameters"""
    match_duration: int = 300  # 5 minutes
    tick_rate: float = 60.0    # 60 FPS
    num_players: int = 10      # 5v5
    cheat_probability: float = 0.3  # 30% chance of cheating
    network_conditions: Dict[str, float] = None
    
    def __post_init__(self):
        if self.network_conditions is None:
            self.network_conditions = {
                'packet_loss': 0.02,  # 2% packet loss
                'latency': 15.0,      # 15ms latency
                'jitter': 5.0,        # 5ms jitter
                'bandwidth': 100.0    # 100 Mbps
            }

class SimulationManager:
    """Manages the Duality AI simulation environment"""
    
    def __init__(self, config: SimulationConfig = None):
        self.config = config or SimulationConfig()
        self.environment = LANEnvironment()
        self.agents: List[Agent] = []
        self.is_running = False
        self.current_tick = 0
        self.match_start_time = None
        self.events = []
        
    async def initialize(self):
        """Initialize the simulation environment"""
        logger.info("🎮 Initializing simulation environment...")
        
        # Initialize LAN environment
        await self.environment.initialize()
        
        # Create agents
        await self._create_agents()
        
        # Set up network conditions
        self.environment.set_network_conditions(self.config.network_conditions)
        
        logger.info(f"✅ Simulation initialized with {len(self.agents)} agents")
    
    async def _create_agents(self):
        """Create AI agents for the simulation"""
        logger.info("🤖 Creating AI agents...")
        
        # Create 5v5 teams
        team_a_players = []
        team_b_players = []
        
        for i in range(5):
            # Team A
            is_cheater = random.random() < self.config.cheat_probability
            agent_a = CheatAgent(f"TeamA_Player{i+1}") if is_cheater else NormalAgent(f"TeamA_Player{i+1}")
            team_a_players.append(agent_a)
            
            # Team B
            is_cheater = random.random() < self.config.cheat_probability
            agent_b = CheatAgent(f"TeamB_Player{i+1}") if is_cheater else NormalAgent(f"TeamB_Player{i+1}")
            team_b_players.append(agent_b)
        
        self.agents = team_a_players + team_b_players
        
        # Initialize agents
        for agent in self.agents:
            await agent.initialize()
            agent.set_environment(self.environment)
        
        logger.info(f"✅ Created {len(self.agents)} agents ({sum(1 for a in self.agents if isinstance(a, CheatAgent))} cheaters)")
    
    async def run_simulation(self):
        """Run the main simulation loop"""
        logger.info("🎯 Starting simulation...")
        
        self.is_running = True
        self.match_start_time = datetime.now()
        self.current_tick = 0
        
        tick_interval = 1.0 / self.config.tick_rate
        
        while self.is_running and self.current_tick < (self.config.match_duration * self.config.tick_rate):
            try:
                # Process tick
                await self._process_tick()
                
                # Update agents
                await self._update_agents()
                
                # Record events
                await self._record_events()
                
                # Check for match end
                if self._should_end_match():
                    break
                
                self.current_tick += 1
                await asyncio.sleep(tick_interval)
                
            except Exception as e:
                logger.error(f"❌ Error in simulation tick: {e}")
                break
        
        await self._end_match()
        logger.info("🏁 Simulation completed")
    
    async def _process_tick(self):
        """Process a single simulation tick"""
        # Update environment
        await self.environment.update()
        
        # Generate network events
        network_events = self.environment.get_network_events()
        for event in network_events:
            self.events.append({
                'tick': self.current_tick,
                'type': 'network',
                'data': event,
                'timestamp': datetime.now()
            })
    
    async def _update_agents(self):
        """Update all agents for current tick"""
        for agent in self.agents:
            try:
                # Get agent action
                action = await agent.get_action()
                
                # Apply action to environment
                result = await self.environment.apply_action(agent, action)
                
                # Record agent event
                self.events.append({
                    'tick': self.current_tick,
                    'type': 'agent_action',
                    'agent_id': agent.id,
                    'action': action,
                    'result': result,
                    'timestamp': datetime.now()
                })
                
            except Exception as e:
                logger.error(f"❌ Error updating agent {agent.id}: {e}")
    
    async def _record_events(self):
        """Record simulation events for analytics"""
        # Record match state
        match_state = {
            'tick': self.current_tick,
            'type': 'match_state',
            'timestamp': datetime.now(),
            'data': {
                'elapsed_time': self.current_tick / self.config.tick_rate,
                'agents_alive': len([a for a in self.agents if a.is_alive]),
                'network_health': self.environment.get_network_health(),
                'performance_metrics': self.environment.get_performance_metrics()
            }
        }
        self.events.append(match_state)
    
    def _should_end_match(self) -> bool:
        """Check if match should end"""
        # End if all players on one team are eliminated
        team_a_alive = sum(1 for a in self.agents[:5] if a.is_alive)
        team_b_alive = sum(1 for a in self.agents[5:] if a.is_alive)
        
        return team_a_alive == 0 or team_b_alive == 0
    
    async def _end_match(self):
        """Handle match end"""
        logger.info("🏁 Ending match...")
        
        # Calculate final statistics
        stats = self._calculate_match_stats()
        
        # Record final event
        self.events.append({
            'tick': self.current_tick,
            'type': 'match_end',
            'timestamp': datetime.now(),
            'data': stats
        })
        
        self.is_running = False
    
    def _calculate_match_stats(self) -> Dict[str, Any]:
        """Calculate final match statistics"""
        team_a_score = sum(agent.score for agent in self.agents[:5])
        team_b_score = sum(agent.score for agent in self.agents[5:])
        
        cheaters_detected = sum(1 for agent in self.agents if isinstance(agent, CheatAgent) and agent.detected)
        
        return {
            'team_a_score': team_a_score,
            'team_b_score': team_b_score,
            'winner': 'Team A' if team_a_score > team_b_score else 'Team B',
            'cheaters_detected': cheaters_detected,
            'total_events': len(self.events),
            'match_duration': self.current_tick / self.config.tick_rate
        }
    
    def get_events(self) -> List[Dict[str, Any]]:
        """Get all recorded events"""
        return self.events.copy()
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current simulation state"""
        return {
            'is_running': self.is_running,
            'current_tick': self.current_tick,
            'elapsed_time': self.current_tick / self.config.tick_rate,
            'agents': [agent.get_state() for agent in self.agents],
            'environment': self.environment.get_state()
        }
    
    async def shutdown(self):
        """Shutdown simulation"""
        logger.info("🛑 Shutting down simulation...")
        self.is_running = False
        
        for agent in self.agents:
            await agent.shutdown()
        
        await self.environment.shutdown()
        logger.info("✅ Simulation shutdown complete") 