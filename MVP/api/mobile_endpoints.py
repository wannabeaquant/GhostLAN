"""
Mobile API Endpoints for GhostLAN SimWorld
FastAPI endpoints for iOS/Android mobile applications
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import logging

from mobile.mobile_app import MobileAppBackend

logger = logging.getLogger(__name__)

# Pydantic models for request/response
class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
    device_id: str
    platform: str

class UserLogin(BaseModel):
    email: str
    password: str
    device_id: str

class UserPreferences(BaseModel):
    notifications_enabled: bool = True
    theme: str = "dark"
    language: str = "en"
    auto_join_matches: bool = False

class NotificationResponse(BaseModel):
    success: bool
    notification_id: Optional[str] = None
    error: Optional[str] = None

# Security
security = HTTPBearer()

# Router
mobile_router = APIRouter(prefix="/mobile", tags=["Mobile API"])

# Dependency to get mobile backend
def get_mobile_backend() -> MobileAppBackend:
    # This would be injected from the main app
    from main import mobile_backend
    return mobile_backend

# Dependency to verify token
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security),
                      mobile_backend: MobileAppBackend = Depends(get_mobile_backend)) -> Dict[str, Any]:
    token = credentials.credentials
    payload = mobile_backend.auth.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@mobile_router.post("/auth/register")
async def register_user(
    user_data: UserRegistration,
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Register new mobile user"""
    try:
        result = await mobile_backend.register_user(
            user_data.username,
            user_data.email,
            user_data.password,
            user_data.device_id,
            user_data.platform
        )
        
        if result['success']:
            return {
                "success": True,
                "user_id": result['user_id'],
                "token": result['token'],
                "user": result['user']
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@mobile_router.post("/auth/login")
async def login_user(
    login_data: UserLogin,
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Login mobile user"""
    try:
        result = await mobile_backend.login_user(
            login_data.email,
            login_data.password,
            login_data.device_id
        )
        
        if result['success']:
            return {
                "success": True,
                "user_id": result['user_id'],
                "token": result['token'],
                "user": result['user']
            }
        else:
            raise HTTPException(status_code=401, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@mobile_router.post("/auth/logout")
async def logout_user(
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Logout mobile user"""
    try:
        await mobile_backend.logout_user(
            payload['user_id'],
            payload['device_id']
        )
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")

@mobile_router.get("/profile")
async def get_user_profile(
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Get user profile"""
    try:
        profile = await mobile_backend.get_user_profile(payload['user_id'])
        if 'error' in profile:
            raise HTTPException(status_code=404, detail=profile['error'])
        return profile
    except Exception as e:
        logger.error(f"Profile error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get profile")

@mobile_router.put("/profile/preferences")
async def update_preferences(
    preferences: UserPreferences,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Update user preferences"""
    try:
        result = await mobile_backend.update_user_preferences(
            payload['user_id'],
            preferences.dict()
        )
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Preferences update error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")

@mobile_router.get("/notifications")
async def get_notifications(
    limit: int = 50,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Get user notifications"""
    try:
        notifications = await mobile_backend.get_notifications(
            payload['user_id'],
            limit
        )
        return {"notifications": notifications}
    except Exception as e:
        logger.error(f"Notifications error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get notifications")

@mobile_router.post("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Mark notification as read"""
    try:
        await mobile_backend.mark_notification_read(notification_id)
        return {"success": True, "message": "Notification marked as read"}
    except Exception as e:
        logger.error(f"Mark read error: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark notification as read")

@mobile_router.get("/matches")
async def get_user_matches(
    limit: int = 20,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Get user matches"""
    try:
        matches = await mobile_backend.get_user_matches(
            payload['user_id'],
            limit
        )
        return {"matches": matches}
    except Exception as e:
        logger.error(f"Matches error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get matches")

@mobile_router.get("/matches/{match_id}")
async def get_match_details(
    match_id: str,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Get match details"""
    try:
        match_details = await mobile_backend.get_match_details(match_id)
        if 'error' in match_details:
            raise HTTPException(status_code=404, detail=match_details['error'])
        return match_details
    except Exception as e:
        logger.error(f"Match details error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get match details")

@mobile_router.get("/tournaments")
async def get_user_tournaments(
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Get user tournaments"""
    try:
        tournaments = await mobile_backend.get_user_tournaments(payload['user_id'])
        return {"tournaments": tournaments}
    except Exception as e:
        logger.error(f"Tournaments error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get tournaments")

@mobile_router.post("/tournaments/{tournament_id}/register")
async def register_for_tournament(
    tournament_id: str,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Register for tournament"""
    try:
        result = await mobile_backend.register_for_tournament(
            tournament_id,
            payload['user_id']
        )
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Tournament registration error: {e}")
        raise HTTPException(status_code=500, detail="Failed to register for tournament")

@mobile_router.get("/tournaments/{tournament_id}/bracket")
async def get_tournament_bracket(
    tournament_id: str,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Get tournament bracket"""
    try:
        bracket = await mobile_backend.get_tournament_bracket(tournament_id)
        if 'error' in bracket:
            raise HTTPException(status_code=404, detail=bracket['error'])
        return bracket
    except Exception as e:
        logger.error(f"Tournament bracket error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get tournament bracket")

@mobile_router.get("/stats")
async def get_user_stats(
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Get user statistics"""
    try:
        stats = await mobile_backend.get_user_stats(payload['user_id'])
        return stats
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user stats")

@mobile_router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 100,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Get global leaderboard"""
    try:
        leaderboard = await mobile_backend.get_leaderboard(limit)
        return {"leaderboard": leaderboard}
    except Exception as e:
        logger.error(f"Leaderboard error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get leaderboard")

@mobile_router.get("/qr-code")
async def generate_qr_code(
    data: str,
    payload: Dict[str, Any] = Depends(verify_token),
    mobile_backend: MobileAppBackend = Depends(get_mobile_backend)
):
    """Generate QR code for mobile app"""
    try:
        qr_code = await mobile_backend.generate_qr_code(data)
        return {"qr_code": qr_code}
    except Exception as e:
        logger.error(f"QR code error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate QR code")

@mobile_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "mobile-api",
        "timestamp": "2024-01-01T00:00:00Z"
    } 