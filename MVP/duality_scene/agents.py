"""
AI Agents for GhostLAN SimWorld
Normal and cheat-prone agent behaviors
"""

import asyncio
import logging
import random
import math
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class AgentState:
    """Current state of an agent"""
    id: str
    position: tuple[float, float, float]  # x, y, z
    health: float = 100.0
    score: int = 0
    kills: int = 0
    deaths: int = 0
    accuracy: float = 0.0
    is_alive: bool = True
    team: str = ""
    last_action: Dict[str, Any] = None

@dataclass
class GameAction:
    """Action that an agent can perform"""
    type: str  # move, shoot, reload, etc.
    target_position: Optional[tuple[float, float, float]] = None
    target_agent: Optional[str] = None
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

class Agent(ABC):
    """Base agent class"""
    
    def __init__(self, agent_id: str, team: str = ""):
        self.id = agent_id
        self.team = team
        self.state = AgentState(id=agent_id, position=(0.0, 0.0, 0.0), team=team)
        self.environment = None
        self.behavior_pattern = "normal"
        self.last_update = datetime.now()
        
    async def initialize(self):
        """Initialize the agent"""
        logger.info(f"🤖 Initializing agent {self.id}")
        self.state.position = self._get_spawn_position()
        
    def set_environment(self, environment):
        """Set the environment reference"""
        self.environment = environment
        
    def _get_spawn_position(self) -> tuple[float, float, float]:
        """Get spawn position based on team"""
        if "TeamA" in self.id:
            return (random.uniform(-50, -10), 0, random.uniform(-50, 50))
        else:
            return (random.uniform(10, 50), 0, random.uniform(-50, 50))
    
    @abstractmethod
    async def get_action(self) -> GameAction:
        """Get the next action for this agent"""
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """Get current agent state"""
        return {
            'id': self.state.id,
            'position': self.state.position,
            'health': self.state.health,
            'score': self.state.score,
            'kills': self.state.kills,
            'deaths': self.state.deaths,
            'accuracy': self.state.accuracy,
            'is_alive': self.state.is_alive,
            'team': self.state.team,
            'behavior_pattern': self.behavior_pattern
        }
    
    def update_state(self, new_state: Dict[str, Any]):
        """Update agent state from environment"""
        for key, value in new_state.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
    
    async def shutdown(self):
        """Shutdown the agent"""
        logger.info(f"🛑 Shutting down agent {self.id}")

class NormalAgent(Agent):
    """Normal agent with realistic gaming behavior"""
    
    def __init__(self, agent_id: str, team: str = ""):
        super().__init__(agent_id, team)
        self.behavior_pattern = "normal"
        self.skill_level = random.uniform(0.3, 0.8)  # Skill level 0-1
        self.reaction_time = random.uniform(0.1, 0.3)  # Seconds
        self.aim_accuracy = random.uniform(0.4, 0.9)  # Base accuracy
        
    async def get_action(self) -> GameAction:
        """Get action for normal agent"""
        if not self.state.is_alive:
            return GameAction(type="wait")
        
        # Basic AI decision making
        action_type = self._choose_action_type()
        
        if action_type == "move":
            return self._get_movement_action()
        elif action_type == "shoot":
            return self._get_shooting_action()
        elif action_type == "reload":
            return GameAction(type="reload")
        else:
            return GameAction(type="wait")
    
    def _choose_action_type(self) -> str:
        """Choose what type of action to perform"""
        # Simple probability-based decision making
        rand = random.random()
        
        if rand < 0.4:  # 40% chance to move
            return "move"
        elif rand < 0.7:  # 30% chance to shoot
            return "shoot"
        elif rand < 0.85:  # 15% chance to reload
            return "reload"
        else:  # 15% chance to wait
            return "wait"
    
    def _get_movement_action(self) -> GameAction:
        """Get movement action"""
        # Simple movement towards enemy or objective
        current_pos = self.state.position
        
        # Find nearest enemy or move towards center
        target_pos = self._find_movement_target()
        
        # Add some randomness to movement
        noise = random.uniform(-5, 5)
        target_pos = (target_pos[0] + noise, target_pos[1], target_pos[2] + noise)
        
        return GameAction(
            type="move",
            target_position=target_pos,
            parameters={"speed": random.uniform(0.5, 1.0)}
        )
    
    def _get_shooting_action(self) -> GameAction:
        """Get shooting action"""
        # Find target to shoot at
        target = self._find_shooting_target()
        
        if target:
            # Apply accuracy based on skill level
            accuracy_modifier = self.aim_accuracy * self.skill_level
            
            # Add some spread to shots
            spread = (1 - accuracy_modifier) * 10
            target_pos = (
                target[0] + random.uniform(-spread, spread),
                target[1] + random.uniform(-spread, spread),
                target[2] + random.uniform(-spread, spread)
            )
            
            return GameAction(
                type="shoot",
                target_position=target_pos,
                target_agent=target.get('id') if isinstance(target, dict) else None
            )
        
        return GameAction(type="wait")
    
    def _find_movement_target(self) -> tuple[float, float, float]:
        """Find target position for movement"""
        # Simple AI: move towards center or enemy spawn
        if "TeamA" in self.id:
            return (random.uniform(0, 30), 0, random.uniform(-30, 30))
        else:
            return (random.uniform(-30, 0), 0, random.uniform(-30, 30))
    
    def _find_shooting_target(self) -> Optional[tuple[float, float, float]]:
        """Find target for shooting"""
        # Simple target finding - simulate line of sight
        if self.environment:
            # Get visible enemies (simplified)
            enemies = self.environment.get_visible_enemies(self.id)
            if enemies:
                return random.choice(enemies)['position']
        
        return None

class CheatAgent(Agent):
    """Agent with cheating behaviors for testing anti-cheat"""
    
    def __init__(self, agent_id: str, team: str = ""):
        super().__init__(agent_id, team)
        self.behavior_pattern = "cheat"
        self.cheat_types = self._select_cheat_types()
        self.detected = False
        self.cheat_confidence = 0.0
        
        # Cheat parameters
        self.aimbot_strength = random.uniform(0.7, 1.0)
        self.wallhack_range = random.uniform(50, 100)
        self.speed_multiplier = random.uniform(1.2, 2.0)
        
    def _select_cheat_types(self) -> List[str]:
        """Select which cheats this agent will use"""
        available_cheats = ["aimbot", "wallhack", "speedhack", "triggerbot", "esp", "bhop"]
        num_cheats = random.randint(1, 4)  # Use 1-4 different cheats
        return random.sample(available_cheats, num_cheats)
    
    async def get_action(self) -> GameAction:
        """Get action for cheating agent"""
        if not self.state.is_alive:
            return GameAction(type="wait")
        
        # Cheating agents are more aggressive
        action_type = self._choose_cheat_action_type()
        
        if action_type == "move":
            return self._get_cheat_movement_action()
        elif action_type == "shoot":
            return self._get_cheat_shooting_action()
        else:
            return GameAction(type="wait")
    
    def _choose_cheat_action_type(self) -> str:
        """Choose action type with cheat bias"""
        rand = random.random()
        
        if rand < 0.3:  # 30% chance to move
            return "move"
        elif rand < 0.8:  # 50% chance to shoot (more aggressive)
            return "shoot"
        else:  # 20% chance to wait
            return "wait"
    
    def _get_cheat_movement_action(self) -> GameAction:
        """Get movement action with speedhack/bhop"""
        current_pos = self.state.position
        target_pos = self._find_cheat_movement_target()
        
        # Apply speedhack if enabled
        speed = 1.0
        if "speedhack" in self.cheat_types:
            speed = self.speed_multiplier
        
        # Apply bhop (bunny hop) if enabled
        if "bhop" in self.cheat_types:
            # Simulate perfect jump timing
            speed *= 1.3  # 30% speed boost from bhop
            parameters = {"speed": speed, "bhop": True}
        else:
            parameters = {"speed": speed}
        
        return GameAction(
            type="move",
            target_position=target_pos,
            parameters=parameters
        )
    
    def _get_cheat_shooting_action(self) -> GameAction:
        """Get shooting action with aimbot/wallhack/triggerbot"""
        target = self._find_cheat_target()
        
        if target:
            target_pos = target['position']
            
            # Apply aimbot if enabled
            if "aimbot" in self.cheat_types:
                # Perfect or near-perfect aim
                spread = (1 - self.aimbot_strength) * 2
                target_pos = (
                    target_pos[0] + random.uniform(-spread, spread),
                    target_pos[1] + random.uniform(-spread, spread),
                    target_pos[2] + random.uniform(-spread, spread)
                )
            
            # Apply triggerbot (auto-shoot when crosshair is on target)
            if "triggerbot" in self.cheat_types:
                # Simulate perfect timing
                self.triggerbot_active = True
            
            return GameAction(
                type="shoot",
                target_position=target_pos,
                target_agent=target.get('id'),
                parameters={"cheat_used": self.cheat_types}
            )
        
        return GameAction(type="wait")
    
    def _find_cheat_movement_target(self) -> tuple[float, float, float]:
        """Find movement target with wallhack awareness"""
        # Use wallhack to find optimal paths
        if "wallhack" in self.cheat_types and self.environment:
            enemies = self.environment.get_all_enemies(self.id, self.wallhack_range)
            if enemies:
                # Move towards nearest enemy
                nearest = min(enemies, key=lambda e: self._distance(self.state.position, e['position']))
                return nearest['position']
        
        # Fallback to normal movement
        return super()._find_movement_target()
    
    def _find_cheat_target(self) -> Optional[Dict[str, Any]]:
        """Find target with wallhack"""
        if self.environment:
            if "wallhack" in self.cheat_types:
                # Can see through walls
                enemies = self.environment.get_all_enemies(self.id, self.wallhack_range)
            else:
                # Normal line of sight
                enemies = self.environment.get_visible_enemies(self.id)
            
            if enemies:
                return random.choice(enemies)
        
        return None
    
    def _distance(self, pos1: tuple[float, float, float], pos2: tuple[float, float, float]) -> float:
        """Calculate distance between two positions"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    
    def get_cheat_signature(self) -> Dict[str, Any]:
        """Get signature of cheating behavior for detection"""
        return {
            'agent_id': self.id,
            'cheat_types': self.cheat_types,
            'confidence': self.cheat_confidence,
            'detected': self.detected,
            'aimbot_strength': self.aimbot_strength,
            'wallhack_range': self.wallhack_range,
            'speed_multiplier': self.speed_multiplier
        } 