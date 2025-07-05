"""
Voice Simulation for GhostLAN SimWorld
Simulates voice chat traffic and voice-based cheat detection
"""

import asyncio
import logging
import random
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class VoicePacket:
    """Voice packet structure"""
    sender_id: str
    timestamp: datetime
    data: bytes
    packet_size: int
    sequence_number: int
    is_voice: bool = True
    quality: float = 1.0

@dataclass
class VoiceChannel:
    """Voice channel configuration"""
    channel_id: str
    participants: List[str]
    codec: str = "opus"
    sample_rate: int = 48000
    bitrate: int = 64000
    packet_loss: float = 0.02
    latency: float = 15.0

class VoiceSimulator:
    """Simulates voice chat traffic and analysis"""
    
    def __init__(self):
        self.channels = {}
        self.voice_packets = []
        self.voice_events = []
        self.sequence_counters = {}
        self.voice_analysis = {
            'total_packets': 0,
            'packets_lost': 0,
            'voice_quality': 1.0,
            'suspicious_activity': []
        }
        
    async def initialize(self):
        """Initialize voice simulation"""
        logger.info("🎤 Initializing Voice Simulation...")
        
        # Create default voice channels
        self.channels['team_a'] = VoiceChannel(
            channel_id='team_a',
            participants=['TeamA_Player1', 'TeamA_Player2', 'TeamA_Player3', 'TeamA_Player4', 'TeamA_Player5']
        )
        
        self.channels['team_b'] = VoiceChannel(
            channel_id='team_b',
            participants=['TeamB_Player1', 'TeamB_Player2', 'TeamB_Player3', 'TeamB_Player4', 'TeamB_Player5']
        )
        
        # Initialize sequence counters
        for participant in self.channels['team_a'].participants + self.channels['team_b'].participants:
            self.sequence_counters[participant] = 0
            
    async def simulate_voice_traffic(self, tick: int):
        """Simulate voice traffic for current tick"""
        voice_events = []
        
        for channel_id, channel in self.channels.items():
            # Simulate voice activity for each participant
            for participant in channel.participants:
                # Random chance of speaking
                if random.random() < 0.3:  # 30% chance of voice activity
                    voice_event = await self._generate_voice_event(participant, channel, tick)
                    voice_events.append(voice_event)
                    
                    # Analyze voice for suspicious activity
                    analysis = self._analyze_voice_activity(voice_event)
                    if analysis['suspicious']:
                        self.voice_analysis['suspicious_activity'].append(analysis)
                        
        self.voice_events.extend(voice_events)
        return voice_events
        
    async def _generate_voice_event(self, participant: str, channel: VoiceChannel, tick: int) -> Dict[str, Any]:
        """Generate a voice event for a participant"""
        # Simulate voice packet
        packet_size = random.randint(20, 200)  # bytes
        sequence_number = self.sequence_counters[participant]
        self.sequence_counters[participant] += 1
        
        # Simulate packet loss
        packet_lost = random.random() < channel.packet_loss
        
        # Simulate voice quality based on network conditions
        base_quality = 1.0
        quality_degradation = random.uniform(0, 0.3)  # Up to 30% quality loss
        final_quality = max(0.1, base_quality - quality_degradation)
        
        voice_event = {
            'tick': tick,
            'timestamp': datetime.now(),
            'type': 'voice_packet',
            'participant': participant,
            'channel': channel.channel_id,
            'packet_size': packet_size,
            'sequence_number': sequence_number,
            'packet_lost': packet_lost,
            'quality': final_quality,
            'latency': channel.latency + random.uniform(-5, 5),  # Add jitter
            'voice_data': self._generate_voice_data(packet_size)
        }
        
        # Update statistics
        self.voice_analysis['total_packets'] += 1
        if packet_lost:
            self.voice_analysis['packets_lost'] += 1
            
        return voice_event
        
    def _generate_voice_data(self, size: int) -> bytes:
        """Generate simulated voice data"""
        # Simulate voice waveform data
        voice_samples = np.random.randint(0, 255, size, dtype=np.uint8)
        return bytes(voice_samples)
        
    def _analyze_voice_activity(self, voice_event: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze voice activity for suspicious behavior"""
        analysis = {
            'suspicious': False,
            'reasons': [],
            'confidence': 0.0
        }
        
        # Check for unusual packet patterns
        if voice_event['packet_size'] > 150:  # Large packets might indicate recording
            analysis['suspicious'] = True
            analysis['reasons'].append('large_packet_size')
            analysis['confidence'] += 0.3
            
        # Check for perfect timing (might indicate automation)
        if voice_event['quality'] > 0.95 and voice_event['packet_size'] > 100:
            analysis['suspicious'] = True
            analysis['reasons'].append('suspicious_quality')
            analysis['confidence'] += 0.4
            
        # Check for rapid sequence numbers (might indicate voice spam)
        if voice_event['sequence_number'] > 1000:  # High sequence might indicate spam
            analysis['suspicious'] = True
            analysis['reasons'].append('high_sequence_number')
            analysis['confidence'] += 0.2
            
        analysis['confidence'] = min(1.0, analysis['confidence'])
        return analysis
        
    def get_voice_statistics(self) -> Dict[str, Any]:
        """Get voice traffic statistics"""
        if self.voice_analysis['total_packets'] == 0:
            return {}
            
        packet_loss_rate = self.voice_analysis['packets_lost'] / self.voice_analysis['total_packets']
        
        return {
            'total_packets': self.voice_analysis['total_packets'],
            'packets_lost': self.voice_analysis['packets_lost'],
            'packet_loss_rate': packet_loss_rate,
            'average_quality': self.voice_analysis['voice_quality'],
            'suspicious_events': len(self.voice_analysis['suspicious_activity']),
            'active_channels': len(self.channels),
            'total_participants': sum(len(ch.participants) for ch in self.channels.values())
        }
        
    def get_voice_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent voice events"""
        return self.voice_events[-limit:] if self.voice_events else []
        
    def get_suspicious_voice_activity(self) -> List[Dict[str, Any]]:
        """Get suspicious voice activity"""
        return self.voice_analysis['suspicious_activity']
        
    def simulate_voice_attack(self, attack_type: str, participant: str):
        """Simulate voice-based attacks"""
        attack_event = {
            'timestamp': datetime.now(),
            'type': 'voice_attack',
            'attack_type': attack_type,
            'participant': participant,
            'description': self._get_attack_description(attack_type)
        }
        
        self.voice_analysis['suspicious_activity'].append({
            'suspicious': True,
            'reasons': [f'voice_attack_{attack_type}'],
            'confidence': 0.9,
            'attack_details': attack_event
        })
        
        logger.warning(f"🎤 Voice attack detected: {attack_type} by {participant}")
        
    def _get_attack_description(self, attack_type: str) -> str:
        """Get description for voice attack type"""
        descriptions = {
            'voice_spam': 'Excessive voice packets detected',
            'voice_recording': 'Suspicious voice recording pattern',
            'voice_injection': 'Voice packet injection detected',
            'voice_eavesdropping': 'Unauthorized voice channel access',
            'voice_manipulation': 'Voice data manipulation detected'
        }
        return descriptions.get(attack_type, 'Unknown voice attack')
        
    async def shutdown(self):
        """Shutdown voice simulation"""
        logger.info("🛑 Shutting down Voice Simulation...")
        self.voice_events.clear()
        self.voice_analysis['suspicious_activity'].clear() 