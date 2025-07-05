"""
GhostLAN Anti-Cheat Engine (Enhanced MVP)
Advanced rule-based and ML-based cheat detection for simulation
"""

import logging
import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import IsolationForest
from collections import defaultdict

logger = logging.getLogger(__name__)

class AntiCheatEngine:
    """Advanced anti-cheat engine for GhostLAN SimWorld"""
    def __init__(self):
        self.detections = []
        self.rules = [
            self.detect_aimbot,
            self.detect_wallhack,
            self.detect_speedhack,
            self.detect_triggerbot,
            self.detect_esp,
            self.detect_bhop
        ]
        self.ml_detector = IsolationForest(contamination=0.1, random_state=42)
        self.agent_stats = defaultdict(lambda: {
            'actions': [],
            'accuracy_history': [],
            'speed_history': [],
            'reaction_times': []
        })
        self.ml_features = []

    async def initialize(self):
        logger.info("🛡️ Initializing Enhanced Anti-Cheat Engine...")

    async def analyze_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a simulation event for cheating"""
        detection_result = {'cheat_detected': False, 'confidence': 0.0, 'rule': None, 'details': {}}
        
        # Update agent statistics
        agent_id = event.get('agent_id')
        if agent_id:
            self._update_agent_stats(agent_id, event)
        
        # Rule-based detection
        for rule in self.rules:
            result = rule(event)
            if result['cheat_detected']:
                detection_result = result
                self.detections.append(result)
                break
        
        # ML-based detection (if we have enough data)
        if len(self.ml_features) > 10:
            ml_result = self._ml_detection(event)
            if ml_result['cheat_detected'] and ml_result['confidence'] > detection_result['confidence']:
                detection_result = ml_result
                self.detections.append(result)
        
        return detection_result

    def _update_agent_stats(self, agent_id: str, event: Dict[str, Any]):
        """Update agent statistics for ML detection"""
        stats = self.agent_stats[agent_id]
        
        if event.get('type') == 'agent_action':
            action = event.get('action', {})
            stats['actions'].append(action.get('type'))
            
            if action.get('type') == 'shoot':
                # Extract accuracy from result
                result = event.get('result', {})
                if 'accuracy' in result:
                    stats['accuracy_history'].append(result['accuracy'])
            
            elif action.get('type') == 'move':
                # Extract speed from parameters
                speed = action.get('parameters', {}).get('speed', 1.0)
                stats['speed_history'].append(speed)
        
        # Keep only recent history
        for key in ['accuracy_history', 'speed_history']:
            if len(stats[key]) > 50:
                stats[key] = stats[key][-50:]

    def _ml_detection(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Machine learning based detection"""
        agent_id = event.get('agent_id')
        if not agent_id or agent_id not in self.agent_stats:
            return {'cheat_detected': False, 'confidence': 0.0, 'rule': 'ml', 'details': {}}
        
        stats = self.agent_stats[agent_id]
        
        # Extract features
        features = []
        if stats['accuracy_history']:
            features.extend([
                np.mean(stats['accuracy_history']),
                np.std(stats['accuracy_history']),
                np.max(stats['accuracy_history'])
            ])
        else:
            features.extend([0.5, 0.1, 0.5])
        
        if stats['speed_history']:
            features.extend([
                np.mean(stats['speed_history']),
                np.std(stats['speed_history']),
                np.max(stats['speed_history'])
            ])
        else:
            features.extend([1.0, 0.1, 1.0])
        
        # Predict anomaly
        try:
            prediction = self.ml_detector.predict([features])[0]
            if prediction == -1:  # Anomaly detected
                confidence = 0.8
                return {
                    'cheat_detected': True,
                    'confidence': confidence,
                    'rule': 'ml_anomaly',
                    'details': {'features': features}
                }
        except Exception as e:
            logger.warning(f"ML detection failed: {e}")
        
        return {'cheat_detected': False, 'confidence': 0.0, 'rule': 'ml', 'details': {}}

    def detect_aimbot(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Detect aimbot based on accuracy patterns"""
        if event.get('type') == 'agent_action' and event.get('action', {}).get('type') == 'shoot':
            accuracy = event.get('agent_state', {}).get('accuracy', 0)
            if accuracy > 0.95:
                return {
                    'cheat_detected': True,
                    'confidence': 0.9,
                    'rule': 'aimbot',
                    'details': {'accuracy': accuracy}
                }
        return {'cheat_detected': False, 'confidence': 0.0, 'rule': None, 'details': {}}

    def detect_wallhack(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Detect wallhack based on shooting through walls"""
        if event.get('type') == 'agent_action' and event.get('action', {}).get('type') == 'shoot':
            if 'wallhack' in event.get('action', {}).get('parameters', {}).get('cheat_used', []):
                return {
                    'cheat_detected': True,
                    'confidence': 0.8,
                    'rule': 'wallhack',
                    'details': {}
                }
        return {'cheat_detected': False, 'confidence': 0.0, 'rule': None, 'details': {}}

    def detect_speedhack(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Detect speedhack based on movement speed"""
        if event.get('type') == 'agent_action' and event.get('action', {}).get('type') == 'move':
            speed = event.get('action', {}).get('parameters', {}).get('speed', 1.0)
            if speed > 1.5:
                return {
                    'cheat_detected': True,
                    'confidence': 0.7,
                    'rule': 'speedhack',
                    'details': {'speed': speed}
                }
        return {'cheat_detected': False, 'confidence': 0.0, 'rule': None, 'details': {}}

    def detect_triggerbot(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Detect triggerbot based on perfect timing"""
        if event.get('type') == 'agent_action' and event.get('action', {}).get('type') == 'shoot':
            if 'triggerbot' in event.get('action', {}).get('parameters', {}).get('cheat_used', []):
                return {
                    'cheat_detected': True,
                    'confidence': 0.75,
                    'rule': 'triggerbot',
                    'details': {}
                }
        return {'cheat_detected': False, 'confidence': 0.0, 'rule': None, 'details': {}}

    def detect_esp(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Detect ESP (Extra Sensory Perception) based on perfect awareness"""
        if event.get('type') == 'agent_action':
            # ESP detection based on perfect enemy awareness
            if 'esp' in event.get('action', {}).get('parameters', {}).get('cheat_used', []):
                return {
                    'cheat_detected': True,
                    'confidence': 0.8,
                    'rule': 'esp',
                    'details': {}
                }
        return {'cheat_detected': False, 'confidence': 0.0, 'rule': None, 'details': {}}

    def detect_bhop(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Detect bunny hop based on movement patterns"""
        if event.get('type') == 'agent_action' and event.get('action', {}).get('type') == 'move':
            if event.get('action', {}).get('parameters', {}).get('bhop', False):
                return {
                    'cheat_detected': True,
                    'confidence': 0.6,
                    'rule': 'bhop',
                    'details': {}
                }
        return {'cheat_detected': False, 'confidence': 0.0, 'rule': None, 'details': {}}

    async def shutdown(self):
        logger.info("🛑 Shutting down Enhanced Anti-Cheat Engine...")

    def get_detections(self) -> List[Dict[str, Any]]:
        return self.detections.copy()

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics for all agents"""
        return dict(self.agent_stats) 