"""
Mobile App Backend for GhostLAN SimWorld
REST API endpoints for iOS/Android mobile applications
"""

import asyncio
import logging
import json
import jwt
import hashlib
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import aiofiles
import qrcode
from io import BytesIO
import base64

logger = logging.getLogger(__name__)

@dataclass
class MobileUser:
    """Mobile user data model"""
    user_id: str
    username: str
    email: str
    device_id: str
    platform: str  # 'ios' or 'android'
    created_at: datetime
    last_login: datetime
    preferences: Dict[str, Any]
    subscription_tier: str = 'free'  # 'free', 'premium', 'pro'

@dataclass
class MobileNotification:
    """Mobile notification data model"""
    notification_id: str
    user_id: str
    title: str
    message: str
    type: str  # 'match', 'tournament', 'alert', 'system'
    data: Dict[str, Any]
    created_at: datetime
    read: bool = False

class MobileAuthentication:
    """Mobile authentication system"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.users = {}
        self.sessions = {}
        self.device_tokens = {}
        
    def generate_token(self, user_id: str, device_id: str) -> str:
        """Generate JWT token for mobile user"""
        payload = {
            'user_id': user_id,
            'device_id': device_id,
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
        
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
            
    async def register_user(self, username: str, email: str, password: str, 
                          device_id: str, platform: str) -> Dict[str, Any]:
        """Register new mobile user"""
        # Check if user already exists
        for user in self.users.values():
            if user.email == email:
                return {'success': False, 'error': 'Email already registered'}
                
        # Create new user
        user_id = hashlib.md5(f"{email}{time.time()}".encode()).hexdigest()
        user = MobileUser(
            user_id=user_id,
            username=username,
            email=email,
            device_id=device_id,
            platform=platform,
            created_at=datetime.utcnow(),
            last_login=datetime.utcnow(),
            preferences={},
            subscription_tier='free'
        )
        
        self.users[user_id] = user
        self.device_tokens[device_id] = user_id
        
        # Generate token
        token = self.generate_token(user_id, device_id)
        
        logger.info(f"📱 New mobile user registered: {username} ({platform})")
        return {
            'success': True,
            'user_id': user_id,
            'token': token,
            'user': asdict(user)
        }
        
    async def login_user(self, email: str, password: str, device_id: str) -> Dict[str, Any]:
        """Login mobile user"""
        # Find user by email
        user = None
        for u in self.users.values():
            if u.email == email:
                user = u
                break
                
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        # Update device and login time
        user.device_id = device_id
        user.last_login = datetime.utcnow()
        self.device_tokens[device_id] = user.user_id
        
        # Generate token
        token = self.generate_token(user.user_id, device_id)
        
        logger.info(f"📱 Mobile user logged in: {user.username}")
        return {
            'success': True,
            'user_id': user.user_id,
            'token': token,
            'user': asdict(user)
        }
        
    async def logout_user(self, user_id: str, device_id: str):
        """Logout mobile user"""
        if device_id in self.device_tokens:
            del self.device_tokens[device_id]
        logger.info(f"📱 Mobile user logged out: {user_id}")

class MobileNotificationService:
    """Mobile notification service"""
    
    def __init__(self):
        self.notifications = {}
        self.push_services = {
            'ios': self._send_ios_push,
            'android': self._send_android_push
        }
        
    async def create_notification(self, user_id: str, title: str, message: str, 
                                notification_type: str, data: Dict[str, Any] = None) -> str:
        """Create new notification"""
        notification_id = hashlib.md5(f"{user_id}{time.time()}".encode()).hexdigest()
        
        notification = MobileNotification(
            notification_id=notification_id,
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            data=data or {},
            created_at=datetime.utcnow()
        )
        
        self.notifications[notification_id] = notification
        
        # Send push notification
        await self._send_push_notification(notification)
        
        logger.info(f"📱 Notification created: {title} for user {user_id}")
        return notification_id
        
    async def _send_push_notification(self, notification: MobileNotification):
        """Send push notification to mobile device"""
        # Simulate push notification sending
        logger.info(f"📱 Push notification sent: {notification.title}")
        
    async def _send_ios_push(self, device_token: str, payload: Dict[str, Any]):
        """Send iOS push notification"""
        # Simulate iOS push
        logger.debug(f"📱 iOS push to {device_token}: {payload}")
        
    async def _send_android_push(self, device_token: str, payload: Dict[str, Any]):
        """Send Android push notification"""
        # Simulate Android push
        logger.debug(f"📱 Android push to {device_token}: {payload}")
        
    async def get_user_notifications(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get notifications for user"""
        user_notifications = [
            asdict(n) for n in self.notifications.values()
            if n.user_id == user_id
        ]
        
        # Sort by creation time (newest first)
        user_notifications.sort(key=lambda x: x['created_at'], reverse=True)
        return user_notifications[:limit]
        
    async def mark_notification_read(self, notification_id: str):
        """Mark notification as read"""
        if notification_id in self.notifications:
            self.notifications[notification_id].read = True

class MobileMatchService:
    """Mobile match service"""
    
    def __init__(self, match_recorder):
        self.match_recorder = match_recorder
        
    async def get_user_matches(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get matches for mobile user"""
        # Get matches from match recorder
        matches = await self.match_recorder.get_matches()
        
        # Filter and format for mobile
        user_matches = []
        for match in matches:
            # Check if user participated in match
            participants = match.get('participants', [])
            if any(p.get('user_id') == user_id for p in participants):
                mobile_match = {
                    'match_id': match['match_id'],
                    'map_name': match.get('map_name', 'Unknown'),
                    'game_mode': match.get('game_mode', '5v5'),
                    'start_time': match.get('start_time'),
                    'duration': match.get('duration'),
                    'result': match.get('result'),
                    'player_stats': next(
                        (p for p in participants if p.get('user_id') == user_id), {}
                    )
                }
                user_matches.append(mobile_match)
                
        return user_matches[:limit]
        
    async def get_match_details(self, match_id: str) -> Dict[str, Any]:
        """Get detailed match information for mobile"""
        match = await self.match_recorder.get_match(match_id)
        if not match:
            return {'error': 'Match not found'}
            
        # Format for mobile consumption
        mobile_match = {
            'match_id': match['match_id'],
            'map_name': match.get('map_name', 'Unknown'),
            'game_mode': match.get('game_mode', '5v5'),
            'start_time': match.get('start_time'),
            'duration': match.get('duration'),
            'result': match.get('result'),
            'participants': match.get('participants', []),
            'events': match.get('events', [])[-50:],  # Last 50 events
            'analytics': match.get('analytics', {})
        }
        
        return mobile_match

class MobileTournamentService:
    """Mobile tournament service"""
    
    def __init__(self, tournament_manager):
        self.tournament_manager = tournament_manager
        
    async def get_user_tournaments(self, user_id: str) -> List[Dict[str, Any]]:
        """Get tournaments for mobile user"""
        tournaments = await self.tournament_manager.get_tournaments()
        
        user_tournaments = []
        for tournament in tournaments:
            # Check if user is registered
            participants = tournament.get('participants', [])
            if any(p.get('user_id') == user_id for p in participants):
                mobile_tournament = {
                    'tournament_id': tournament['tournament_id'],
                    'name': tournament['name'],
                    'status': tournament['status'],
                    'start_date': tournament['start_date'],
                    'end_date': tournament['end_date'],
                    'prize_pool': tournament.get('prize_pool', 0),
                    'participant_count': len(participants),
                    'user_position': self._get_user_position(tournament, user_id)
                }
                user_tournaments.append(mobile_tournament)
                
        return user_tournaments
        
    def _get_user_position(self, tournament: Dict[str, Any], user_id: str) -> Optional[int]:
        """Get user position in tournament"""
        leaderboard = tournament.get('leaderboard', [])
        for i, entry in enumerate(leaderboard):
            if entry.get('user_id') == user_id:
                return i + 1
        return None
        
    async def register_for_tournament(self, tournament_id: str, user_id: str) -> Dict[str, Any]:
        """Register user for tournament"""
        return await self.tournament_manager.register_participant(tournament_id, user_id)
        
    async def get_tournament_bracket(self, tournament_id: str) -> Dict[str, Any]:
        """Get tournament bracket for mobile"""
        tournament = await self.tournament_manager.get_tournament(tournament_id)
        if not tournament:
            return {'error': 'Tournament not found'}
            
        return {
            'tournament_id': tournament_id,
            'bracket': tournament.get('bracket', {}),
            'matches': tournament.get('matches', []),
            'status': tournament['status']
        }

class MobileAnalyticsService:
    """Mobile analytics service"""
    
    def __init__(self, analytics_pipeline):
        self.analytics_pipeline = analytics_pipeline
        
    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics for mobile"""
        # Get user statistics from analytics pipeline
        stats = await self.analytics_pipeline.get_player_stats(user_id)
        
        # Format for mobile
        mobile_stats = {
            'user_id': user_id,
            'total_matches': stats.get('total_matches', 0),
            'wins': stats.get('wins', 0),
            'losses': stats.get('losses', 0),
            'win_rate': stats.get('win_rate', 0.0),
            'average_kills': stats.get('average_kills', 0.0),
            'average_deaths': stats.get('average_deaths', 0.0),
            'average_assists': stats.get('average_assists', 0.0),
            'rank': stats.get('rank', 'Unranked'),
            'rank_points': stats.get('rank_points', 0),
            'recent_performance': stats.get('recent_performance', [])
        }
        
        return mobile_stats
        
    async def get_leaderboard(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get global leaderboard for mobile"""
        leaderboard = await self.analytics_pipeline.get_leaderboard()
        
        # Format for mobile
        mobile_leaderboard = []
        for entry in leaderboard[:limit]:
            mobile_entry = {
                'rank': entry.get('rank', 0),
                'user_id': entry.get('user_id', ''),
                'username': entry.get('username', 'Unknown'),
                'rank_points': entry.get('rank_points', 0),
                'win_rate': entry.get('win_rate', 0.0),
                'total_matches': entry.get('total_matches', 0)
            }
            mobile_leaderboard.append(mobile_entry)
            
        return mobile_leaderboard

class MobileAppBackend:
    """Main mobile app backend"""
    
    def __init__(self, secret_key: str, match_recorder, tournament_manager, analytics_pipeline):
        self.auth = MobileAuthentication(secret_key)
        self.notifications = MobileNotificationService()
        self.matches = MobileMatchService(match_recorder)
        self.tournaments = MobileTournamentService(tournament_manager)
        self.analytics = MobileAnalyticsService(analytics_pipeline)
        
    async def register_user(self, username: str, email: str, password: str, 
                          device_id: str, platform: str) -> Dict[str, Any]:
        """Register new mobile user"""
        return await self.auth.register_user(username, email, password, device_id, platform)
        
    async def login_user(self, email: str, password: str, device_id: str) -> Dict[str, Any]:
        """Login mobile user"""
        return await self.auth.login_user(email, password, device_id)
        
    async def logout_user(self, user_id: str, device_id: str):
        """Logout mobile user"""
        await self.auth.logout_user(user_id, device_id)
        
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        user = self.auth.users.get(user_id)
        if not user:
            return {'error': 'User not found'}
            
        return asdict(user)
        
    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Update user preferences"""
        user = self.auth.users.get(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}
            
        user.preferences.update(preferences)
        return {'success': True, 'preferences': user.preferences}
        
    async def get_notifications(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user notifications"""
        return await self.notifications.get_user_notifications(user_id, limit)
        
    async def mark_notification_read(self, notification_id: str):
        """Mark notification as read"""
        await self.notifications.mark_notification_read(notification_id)
        
    async def get_user_matches(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user matches"""
        return await self.matches.get_user_matches(user_id, limit)
        
    async def get_match_details(self, match_id: str) -> Dict[str, Any]:
        """Get match details"""
        return await self.matches.get_match_details(match_id)
        
    async def get_user_tournaments(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user tournaments"""
        return await self.tournaments.get_user_tournaments(user_id)
        
    async def register_for_tournament(self, tournament_id: str, user_id: str) -> Dict[str, Any]:
        """Register for tournament"""
        return await self.tournaments.register_for_tournament(tournament_id, user_id)
        
    async def get_tournament_bracket(self, tournament_id: str) -> Dict[str, Any]:
        """Get tournament bracket"""
        return await self.tournaments.get_tournament_bracket(tournament_id)
        
    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics"""
        return await self.analytics.get_user_stats(user_id)
        
    async def get_leaderboard(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get global leaderboard"""
        return await self.analytics.get_leaderboard(limit)
        
    async def generate_qr_code(self, data: str) -> str:
        """Generate QR code for mobile app"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
        
    async def shutdown(self):
        """Shutdown mobile app backend"""
        logger.info("🛑 Shutting down Mobile App Backend...") 