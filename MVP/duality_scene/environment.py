"""
LAN Environment for GhostLAN SimWorld
Digital twin of LAN venue with network simulation
"""

import asyncio
import logging
import random
import math
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class NetworkConditions:
    """Network conditions for simulation"""
    packet_loss: float = 0.02  # 2% packet loss
    latency: float = 15.0      # 15ms latency
    jitter: float = 5.0        # 5ms jitter
    bandwidth: float = 100.0   # 100 Mbps
    interference: float = 0.0  # Interference level

@dataclass
class MapGeometry:
    """Map geometry and obstacles"""
    bounds: Tuple[float, float, float, float]  # x_min, x_max, z_min, z_max
    obstacles: List[Dict[str, Any]] = None
    spawn_points: List[Tuple[float, float, float]] = None
    
    def __post_init__(self):
        if self.obstacles is None:
            self.obstacles = []
        if self.spawn_points is None:
            self.spawn_points = []

class LANEnvironment:
    """Digital twin of LAN venue environment"""
    
    def __init__(self):
        self.network_conditions = NetworkConditions()
        self.map_geometry = self._create_default_map()
        self.agents = {}
        self.network_events = []
        self.performance_metrics = {
            'fps': 60.0,
            'cpu_usage': 0.0,
            'memory_usage': 0.0,
            'network_health': 1.0
        }
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the environment"""
        logger.info("🏢 Initializing LAN environment...")
        
        # Set up map geometry
        self._setup_map_geometry()
        
        # Initialize network simulation
        self._initialize_network()
        
        self.is_initialized = True
        logger.info("✅ LAN environment initialized")
    
    def _create_default_map(self) -> MapGeometry:
        """Create default café LAN map"""
        return MapGeometry(
            bounds=(-100, 100, -100, 100),  # 200x200 unit map
            obstacles=[
                # Center wall
                {'type': 'wall', 'position': (0, 0, 0), 'size': (2, 10, 50)},
                # Cover objects
                {'type': 'cover', 'position': (-30, 0, -20), 'size': (5, 3, 5)},
                {'type': 'cover', 'position': (30, 0, 20), 'size': (5, 3, 5)},
                {'type': 'cover', 'position': (-20, 0, 30), 'size': (5, 3, 5)},
                {'type': 'cover', 'position': (20, 0, -30), 'size': (5, 3, 5)},
            ],
            spawn_points=[
                # Team A spawns
                (-80, 0, -80), (-80, 0, -40), (-80, 0, 0), (-80, 0, 40), (-80, 0, 80),
                # Team B spawns
                (80, 0, -80), (80, 0, -40), (80, 0, 0), (80, 0, 40), (80, 0, 80)
            ]
        )
    
    def _setup_map_geometry(self):
        """Set up map geometry and collision detection"""
        # Add more detailed obstacles for realistic gameplay
        additional_obstacles = [
            # Computer stations (simplified as walls)
            {'type': 'station', 'position': (-60, 0, -60), 'size': (10, 2, 10)},
            {'type': 'station', 'position': (-60, 0, 0), 'size': (10, 2, 10)},
            {'type': 'station', 'position': (-60, 0, 60), 'size': (10, 2, 10)},
            {'type': 'station', 'position': (60, 0, -60), 'size': (10, 2, 10)},
            {'type': 'station', 'position': (60, 0, 0), 'size': (10, 2, 10)},
            {'type': 'station', 'position': (60, 0, 60), 'size': (10, 2, 10)},
        ]
        
        self.map_geometry.obstacles.extend(additional_obstacles)
    
    def _initialize_network(self):
        """Initialize network simulation"""
        # Set up network event generation
        self.network_event_timer = 0
        self.network_event_interval = random.uniform(1.0, 5.0)  # Events every 1-5 seconds
    
    def set_network_conditions(self, conditions: Dict[str, float]):
        """Update network conditions"""
        for key, value in conditions.items():
            if hasattr(self.network_conditions, key):
                setattr(self.network_conditions, key, value)
        
        logger.info(f"🌐 Network conditions updated: {conditions}")
    
    def add_agent(self, agent_id: str, agent_data: Dict[str, Any]):
        """Add agent to environment"""
        self.agents[agent_id] = agent_data
    
    def remove_agent(self, agent_id: str):
        """Remove agent from environment"""
        if agent_id in self.agents:
            del self.agents[agent_id]
    
    async def update(self):
        """Update environment state"""
        # Update network simulation
        await self._update_network()
        
        # Update performance metrics
        self._update_performance_metrics()
        
        # Clear old network events
        self._cleanup_old_events()
    
    async def _update_network(self):
        """Update network simulation"""
        # Simulate network events
        if random.random() < self.network_conditions.packet_loss:
            self._generate_packet_loss_event()
        
        # Simulate latency spikes
        if random.random() < 0.1:  # 10% chance of latency spike
            self._generate_latency_spike()
        
        # Simulate bandwidth issues
        if random.random() < 0.05:  # 5% chance of bandwidth issue
            self._generate_bandwidth_event()
    
    def _generate_packet_loss_event(self):
        """Generate packet loss event"""
        event = {
            'type': 'packet_loss',
            'timestamp': datetime.now(),
            'severity': random.uniform(0.1, 0.5),
            'affected_agents': random.sample(list(self.agents.keys()), 
                                           min(3, len(self.agents)))
        }
        self.network_events.append(event)
    
    def _generate_latency_spike(self):
        """Generate latency spike event"""
        event = {
            'type': 'latency_spike',
            'timestamp': datetime.now(),
            'latency_increase': random.uniform(10, 50),  # ms
            'duration': random.uniform(0.5, 2.0)  # seconds
        }
        self.network_events.append(event)
    
    def _generate_bandwidth_event(self):
        """Generate bandwidth issue event"""
        event = {
            'type': 'bandwidth_issue',
            'timestamp': datetime.now(),
            'bandwidth_reduction': random.uniform(0.2, 0.8),  # 20-80% reduction
            'duration': random.uniform(1.0, 5.0)  # seconds
        }
        self.network_events.append(event)
    
    def _update_performance_metrics(self):
        """Update performance metrics"""
        # Simulate performance variations
        self.performance_metrics['fps'] = max(30, 60 - random.uniform(0, 20))
        self.performance_metrics['cpu_usage'] = min(100, random.uniform(20, 80))
        self.performance_metrics['memory_usage'] = min(100, random.uniform(30, 70))
        
        # Network health based on conditions
        network_health = 1.0
        network_health -= self.network_conditions.packet_loss * 2
        network_health -= self.network_conditions.jitter / 100
        network_health = max(0.0, min(1.0, network_health))
        
        self.performance_metrics['network_health'] = network_health
    
    def _cleanup_old_events(self):
        """Remove old network events"""
        current_time = datetime.now()
        cutoff_time = current_time.timestamp() - 60  # Keep last 60 seconds
        
        self.network_events = [
            event for event in self.network_events
            if event['timestamp'].timestamp() > cutoff_time
        ]
    
    async def apply_action(self, agent, action) -> Dict[str, Any]:
        """Apply agent action to environment"""
        result = {
            'success': True,
            'effects': [],
            'network_impact': None
        }
        
        if action.type == "move":
            result = await self._apply_movement(agent, action)
        elif action.type == "shoot":
            result = await self._apply_shooting(agent, action)
        elif action.type == "reload":
            result = await self._apply_reload(agent, action)
        
        # Add network impact
        result['network_impact'] = self._calculate_network_impact(action)
        
        return result
    
    async def _apply_movement(self, agent, action) -> Dict[str, Any]:
        """Apply movement action"""
        target_pos = action.target_position
        speed = action.parameters.get('speed', 1.0)
        
        # Check collision with obstacles
        if self._check_collision(agent.state.position, target_pos):
            return {
                'success': False,
                'effects': ['collision'],
                'message': 'Movement blocked by obstacle'
            }
        
        # Apply movement with network conditions
        movement_delay = self.network_conditions.latency / 1000  # Convert to seconds
        await asyncio.sleep(movement_delay)
        
        # Update agent position
        agent.state.position = target_pos
        
        return {
            'success': True,
            'effects': ['moved'],
            'new_position': target_pos
        }
    
    async def _apply_shooting(self, agent, action) -> Dict[str, Any]:
        """Apply shooting action"""
        target_pos = action.target_position
        target_agent_id = action.target_agent
        
        # Calculate hit probability based on accuracy and network conditions
        base_accuracy = 0.8
        network_penalty = self.network_conditions.packet_loss * 2
        final_accuracy = max(0.1, base_accuracy - network_penalty)
        
        hit = random.random() < final_accuracy
        
        if hit and target_agent_id and target_agent_id in self.agents:
            # Apply damage to target
            damage = random.uniform(20, 50)
            # This would update the target agent's health
            result = {
                'success': True,
                'effects': ['hit', 'damage_dealt'],
                'damage': damage,
                'target': target_agent_id
            }
        else:
            result = {
                'success': True,
                'effects': ['miss'],
                'accuracy': final_accuracy
            }
        
        return result
    
    async def _apply_reload(self, agent, action) -> Dict[str, Any]:
        """Apply reload action"""
        reload_time = 2.0  # 2 seconds
        await asyncio.sleep(reload_time)
        
        return {
            'success': True,
            'effects': ['reloaded'],
            'reload_time': reload_time
        }
    
    def _check_collision(self, start_pos: Tuple[float, float, float], 
                        end_pos: Tuple[float, float, float]) -> bool:
        """Check for collision with obstacles"""
        # Simple collision detection
        for obstacle in self.map_geometry.obstacles:
            if self._line_intersects_box(start_pos, end_pos, obstacle):
                return True
        return False
    
    def _line_intersects_box(self, start: Tuple[float, float, float], 
                           end: Tuple[float, float, float], 
                           box: Dict[str, Any]) -> bool:
        """Check if line intersects with bounding box"""
        # Simplified collision detection
        box_pos = box['position']
        box_size = box['size']
        
        # Check if either endpoint is inside the box
        for pos in [start, end]:
            if (abs(pos[0] - box_pos[0]) < box_size[0]/2 and
                abs(pos[1] - box_pos[1]) < box_size[1]/2 and
                abs(pos[2] - box_pos[2]) < box_size[2]/2):
                return True
        
        return False
    
    def _calculate_network_impact(self, action) -> Dict[str, Any]:
        """Calculate network impact of action"""
        base_latency = self.network_conditions.latency
        jitter = random.uniform(-self.network_conditions.jitter, 
                               self.network_conditions.jitter)
        
        return {
            'latency': base_latency + jitter,
            'packet_loss': self.network_conditions.packet_loss,
            'bandwidth_used': random.uniform(0.1, 1.0)  # MB
        }
    
    def get_visible_enemies(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get enemies visible to agent (line of sight)"""
        if agent_id not in self.agents:
            return []
        
        agent_pos = self.agents[agent_id]['position']
        visible_enemies = []
        
        for enemy_id, enemy_data in self.agents.items():
            if enemy_id == agent_id:
                continue
            
            # Check if enemy is in line of sight
            if self._has_line_of_sight(agent_pos, enemy_data['position']):
                visible_enemies.append({
                    'id': enemy_id,
                    'position': enemy_data['position'],
                    'health': enemy_data.get('health', 100)
                })
        
        return visible_enemies
    
    def get_all_enemies(self, agent_id: str, range_limit: float = 100.0) -> List[Dict[str, Any]]:
        """Get all enemies within range (for wallhack simulation)"""
        if agent_id not in self.agents:
            return []
        
        agent_pos = self.agents[agent_id]['position']
        enemies = []
        
        for enemy_id, enemy_data in self.agents.items():
            if enemy_id == agent_id:
                continue
            
            distance = self._distance(agent_pos, enemy_data['position'])
            if distance <= range_limit:
                enemies.append({
                    'id': enemy_id,
                    'position': enemy_data['position'],
                    'health': enemy_data.get('health', 100),
                    'distance': distance
                })
        
        return enemies
    
    def _has_line_of_sight(self, pos1: Tuple[float, float, float], 
                          pos2: Tuple[float, float, float]) -> bool:
        """Check if there's line of sight between two positions"""
        # Simplified line of sight - just check distance
        distance = self._distance(pos1, pos2)
        return distance < 50  # 50 unit visibility range
    
    def _distance(self, pos1: Tuple[float, float, float], 
                 pos2: Tuple[float, float, float]) -> float:
        """Calculate distance between two positions"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    
    def get_network_events(self) -> List[Dict[str, Any]]:
        """Get recent network events"""
        return self.network_events.copy()
    
    def get_network_health(self) -> float:
        """Get current network health score"""
        return self.performance_metrics['network_health']
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        return self.performance_metrics.copy()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current environment state"""
        return {
            'network_conditions': {
                'packet_loss': self.network_conditions.packet_loss,
                'latency': self.network_conditions.latency,
                'jitter': self.network_conditions.jitter,
                'bandwidth': self.network_conditions.bandwidth
            },
            'performance_metrics': self.performance_metrics,
            'agents_count': len(self.agents),
            'map_bounds': self.map_geometry.bounds
        }
    
    async def shutdown(self):
        """Shutdown environment"""
        logger.info("🛑 Shutting down LAN environment...")
        self.is_initialized = False 