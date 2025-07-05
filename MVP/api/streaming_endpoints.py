"""
Streaming API Endpoints for GhostLAN SimWorld
FastAPI endpoints for real-time streaming and broadcasting
"""

from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import logging
import json

from streaming.real_time_streaming import StreamConfig, RealTimeStreamingSystem

logger = logging.getLogger(__name__)

# Pydantic models
class StreamCreateRequest(BaseModel):
    stream_id: str
    protocol: str = "webrtc"  # 'webrtc', 'rtmp', 'hls'
    quality: str = "high"     # 'low', 'medium', 'high', 'ultra'
    fps: int = 30
    bitrate: int = 5000
    resolution_width: int = 1920
    resolution_height: int = 1080
    audio_enabled: bool = True
    chat_enabled: bool = True

class StreamUpdateRequest(BaseModel):
    quality: Optional[str] = None
    fps: Optional[int] = None
    bitrate: Optional[int] = None
    audio_enabled: Optional[bool] = None
    chat_enabled: Optional[bool] = None

class ChatMessage(BaseModel):
    user_id: str
    username: str
    message: str

class ViewerJoinRequest(BaseModel):
    viewer_id: str
    username: str
    protocol: str = "webrtc"

# Router
streaming_router = APIRouter(prefix="/streaming", tags=["Real-time Streaming"])

# Dependency to get streaming system
def get_streaming_system() -> RealTimeStreamingSystem:
    # This would be injected from the main app
    from main import streaming_system
    return streaming_system

@streaming_router.post("/streams")
async def create_stream(
    request: StreamCreateRequest,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Create new stream"""
    try:
        config = StreamConfig(
            protocol=request.protocol,
            quality=request.quality,
            fps=request.fps,
            bitrate=request.bitrate,
            resolution=(request.resolution_width, request.resolution_height),
            audio_enabled=request.audio_enabled,
            chat_enabled=request.chat_enabled
        )
        
        result = await streaming_system.create_stream(request.stream_id, config)
        
        return {
            "success": True,
            "message": f"Stream {request.stream_id} created successfully",
            "stream": result
        }
        
    except Exception as e:
        logger.error(f"Failed to create stream: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.post("/streams/{stream_id}/start")
async def start_stream(
    stream_id: str,
    rtmp_url: Optional[str] = None,
    output_dir: Optional[str] = None,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Start streaming"""
    try:
        kwargs = {}
        if rtmp_url:
            kwargs['rtmp_url'] = rtmp_url
        if output_dir:
            kwargs['output_dir'] = output_dir
            
        result = await streaming_system.start_stream(stream_id, **kwargs)
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": f"Stream {stream_id} started successfully",
            "stream_id": stream_id
        }
        
    except Exception as e:
        logger.error(f"Failed to start stream: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.post("/streams/{stream_id}/stop")
async def stop_stream(
    stream_id: str,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Stop streaming"""
    try:
        result = await streaming_system.stop_stream(stream_id)
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": f"Stream {stream_id} stopped successfully",
            "stream_id": stream_id
        }
        
    except Exception as e:
        logger.error(f"Failed to stop stream: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.put("/streams/{stream_id}")
async def update_stream(
    stream_id: str,
    request: StreamUpdateRequest,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Update stream configuration"""
    try:
        # Get current stream info
        stream_info = await streaming_system.get_stream_info(stream_id)
        if 'error' in stream_info:
            raise HTTPException(status_code=404, detail=stream_info['error'])
            
        # Update configuration
        config = stream_info['config']
        if request.quality:
            config.quality = request.quality
        if request.fps:
            config.fps = request.fps
        if request.bitrate:
            config.bitrate = request.bitrate
        if request.audio_enabled is not None:
            config.audio_enabled = request.audio_enabled
        if request.chat_enabled is not None:
            config.chat_enabled = request.chat_enabled
            
        return {
            "success": True,
            "message": f"Stream {stream_id} updated successfully",
            "stream_id": stream_id,
            "config": {
                "quality": config.quality,
                "fps": config.fps,
                "bitrate": config.bitrate,
                "audio_enabled": config.audio_enabled,
                "chat_enabled": config.chat_enabled
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to update stream: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.post("/streams/{stream_id}/viewers")
async def add_viewer(
    stream_id: str,
    request: ViewerJoinRequest,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Add viewer to stream"""
    try:
        result = await streaming_system.add_viewer(
            stream_id, 
            request.viewer_id, 
            request.protocol
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": f"Viewer {request.username} added to stream {stream_id}",
            "viewer_id": request.viewer_id,
            "stream_id": stream_id,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Failed to add viewer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.delete("/streams/{stream_id}/viewers/{viewer_id}")
async def remove_viewer(
    stream_id: str,
    viewer_id: str,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Remove viewer from stream"""
    try:
        await streaming_system.remove_viewer(stream_id, viewer_id)
        
        return {
            "success": True,
            "message": f"Viewer {viewer_id} removed from stream {stream_id}",
            "viewer_id": viewer_id,
            "stream_id": stream_id
        }
        
    except Exception as e:
        logger.error(f"Failed to remove viewer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.get("/streams/{stream_id}")
async def get_stream_info(
    stream_id: str,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Get stream information"""
    try:
        stream_info = await streaming_system.get_stream_info(stream_id)
        
        if 'error' in stream_info:
            raise HTTPException(status_code=404, detail=stream_info['error'])
            
        return stream_info
        
    except Exception as e:
        logger.error(f"Failed to get stream info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.get("/streams")
async def list_streams(
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """List all active streams"""
    try:
        streams = await streaming_system.list_streams()
        
        return {
            "streams": streams,
            "count": len(streams)
        }
        
    except Exception as e:
        logger.error(f"Failed to list streams: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoints
@streaming_router.post("/streams/{stream_id}/chat/join")
async def join_chat(
    stream_id: str,
    user_id: str,
    username: str,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Join stream chat"""
    try:
        result = await streaming_system.join_chat(stream_id, user_id, username)
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": f"Joined chat for stream {stream_id}",
            "stream_id": stream_id,
            "user_id": user_id
        }
        
    except Exception as e:
        logger.error(f"Failed to join chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.post("/streams/{stream_id}/chat/messages")
async def send_chat_message(
    stream_id: str,
    message: ChatMessage,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Send chat message"""
    try:
        result = await streaming_system.send_chat_message(
            stream_id, 
            message.user_id, 
            message.message
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
            
        return {
            "success": True,
            "message": "Chat message sent successfully",
            "message_id": result.get('message_id'),
            "stream_id": stream_id
        }
        
    except Exception as e:
        logger.error(f"Failed to send chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.get("/streams/{stream_id}/chat/messages")
async def get_chat_messages(
    stream_id: str,
    limit: int = 50,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Get chat messages"""
    try:
        messages = await streaming_system.get_chat_messages(stream_id, limit)
        
        return {
            "messages": messages,
            "count": len(messages),
            "stream_id": stream_id
        }
        
    except Exception as e:
        logger.error(f"Failed to get chat messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@streaming_router.post("/streams/{stream_id}/chat/messages/{message_id}/read")
async def mark_message_read(
    stream_id: str,
    message_id: str,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """Mark chat message as read"""
    try:
        await streaming_system.mark_notification_read(message_id)
        
        return {
            "success": True,
            "message": "Message marked as read",
            "message_id": message_id,
            "stream_id": stream_id
        }
        
    except Exception as e:
        logger.error(f"Failed to mark message as read: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time streaming
@streaming_router.websocket("/streams/{stream_id}/ws")
async def stream_websocket(
    websocket: WebSocket,
    stream_id: str,
    streaming_system: RealTimeStreamingSystem = Depends(get_streaming_system)
):
    """WebSocket endpoint for real-time streaming"""
    await websocket.accept()
    
    try:
        # Send stream info
        stream_info = await streaming_system.get_stream_info(stream_id)
        await websocket.send_text(json.dumps({
            "type": "stream_info",
            "data": stream_info
        }))
        
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "join":
                # Handle viewer join
                result = await streaming_system.add_viewer(
                    stream_id, 
                    message["viewer_id"], 
                    message.get("protocol", "webrtc")
                )
                await websocket.send_text(json.dumps({
                    "type": "join_response",
                    "data": result
                }))
                
            elif message["type"] == "chat":
                # Handle chat message
                result = await streaming_system.send_chat_message(
                    stream_id,
                    message["user_id"],
                    message["message"]
                )
                await websocket.send_text(json.dumps({
                    "type": "chat_response",
                    "data": result
                }))
                
            elif message["type"] == "ping":
                # Handle ping
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": "2024-01-01T00:00:00Z"
                }))
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for stream {stream_id}")
    except Exception as e:
        logger.error(f"WebSocket error for stream {stream_id}: {e}")
        await websocket.close()

@streaming_router.get("/health")
async def streaming_health_check():
    """Health check for streaming service"""
    return {
        "status": "healthy",
        "service": "streaming-api",
        "timestamp": "2024-01-01T00:00:00Z"
    } 