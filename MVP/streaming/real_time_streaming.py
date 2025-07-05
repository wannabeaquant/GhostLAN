"""
Real-time Streaming System for GhostLAN SimWorld
Live match broadcasting with multiple streaming protocols
"""

import asyncio
import logging
import json
import cv2
import numpy as np
from typing import Dict, Any, List, Optional, Callable
import websockets
import aiohttp
from dataclasses import dataclass
import threading
import time
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

@dataclass
class StreamConfig:
    """Configuration for streaming"""
    protocol: str  # 'webrtc', 'rtmp', 'hls'
    quality: str   # 'low', 'medium', 'high', 'ultra'
    fps: int
    bitrate: int
    resolution: tuple
    audio_enabled: bool = True
    chat_enabled: bool = True

class WebRTCStreamer:
    """WebRTC streaming implementation"""
    
    def __init__(self, config: StreamConfig):
        self.config = config
        self.peers = {}
        self.media_streams = {}
        self.is_streaming = False
        
    async def create_offer(self, peer_id: str) -> Dict[str, Any]:
        """Create WebRTC offer for peer"""
        offer = {
            'type': 'offer',
            'sdp': f'v=0\r\no=- {peer_id} 2 IN IP4 127.0.0.1\r\ns=GhostLAN Stream\r\nt=0 0\r\na=group:BUNDLE 0\r\na=msid-semantic: WMS\r\nm=video 9 UDP/TLS/RTP/SAVPF 96\r\nc=IN IP4 0.0.0.0\r\na=mid:0\r\na=sendonly\r\na=msid:{peer_id} video\r\na=rtpmap:96 H264/90000\r\na=fmtp:96 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f\r\n',
            'peer_id': peer_id
        }
        
        self.peers[peer_id] = {
            'offer': offer,
            'connected': False,
            'last_heartbeat': time.time()
        }
        
        logger.info(f"📡 WebRTC offer created for peer {peer_id}")
        return offer
        
    async def handle_answer(self, peer_id: str, answer: Dict[str, Any]):
        """Handle WebRTC answer from peer"""
        if peer_id in self.peers:
            self.peers[peer_id]['answer'] = answer
            self.peers[peer_id]['connected'] = True
            logger.info(f"✅ WebRTC connection established with peer {peer_id}")
            
    async def send_frame(self, frame: np.ndarray, peer_id: str):
        """Send video frame to peer"""
        if peer_id in self.peers and self.peers[peer_id]['connected']:
            # Encode frame to H.264
            encoded_frame = self._encode_frame(frame)
            # Send via WebRTC data channel
            await self._send_webrtc_data(peer_id, encoded_frame)
            
    def _encode_frame(self, frame: np.ndarray) -> bytes:
        """Encode frame to H.264 format"""
        # Resize frame to target resolution
        resized = cv2.resize(frame, self.config.resolution)
        
        # Convert to H.264 (simplified - in real implementation would use proper encoder)
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter('temp.mp4', fourcc, self.config.fps, self.config.resolution)
        out.write(resized)
        out.release()
        
        # Read encoded data
        with open('temp.mp4', 'rb') as f:
            encoded_data = f.read()
            
        return encoded_data
        
    async def _send_webrtc_data(self, peer_id: str, data: bytes):
        """Send data via WebRTC data channel"""
        # Simulate WebRTC data channel transmission
        logger.debug(f"📤 Sending {len(data)} bytes to peer {peer_id}")

class RTMPStreamer:
    """RTMP streaming implementation"""
    
    def __init__(self, config: StreamConfig):
        self.config = config
        self.rtmp_url = None
        self.is_streaming = False
        self.video_writer = None
        
    async def start_stream(self, rtmp_url: str):
        """Start RTMP stream"""
        self.rtmp_url = rtmp_url
        self.is_streaming = True
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        self.video_writer = cv2.VideoWriter(
            rtmp_url, fourcc, self.config.fps, self.config.resolution
        )
        
        logger.info(f"📡 RTMP stream started: {rtmp_url}")
        
    async def send_frame(self, frame: np.ndarray):
        """Send frame to RTMP stream"""
        if self.is_streaming and self.video_writer:
            # Resize frame to target resolution
            resized = cv2.resize(frame, self.config.resolution)
            self.video_writer.write(resized)
            
    async def stop_stream(self):
        """Stop RTMP stream"""
        if self.video_writer:
            self.video_writer.release()
        self.is_streaming = False
        logger.info("🛑 RTMP stream stopped")

class HLSStreamer:
    """HLS streaming implementation"""
    
    def __init__(self, config: StreamConfig):
        self.config = config
        self.segment_duration = 4  # seconds
        self.segments = []
        self.current_segment = []
        self.segment_counter = 0
        self.is_streaming = False
        
    async def start_stream(self, output_dir: str):
        """Start HLS stream"""
        self.output_dir = output_dir
        self.is_streaming = True
        self.segment_counter = 0
        
        # Create playlist file
        self.playlist_path = f"{output_dir}/playlist.m3u8"
        await self._create_playlist()
        
        logger.info(f"📡 HLS stream started: {output_dir}")
        
    async def send_frame(self, frame: np.ndarray):
        """Add frame to current HLS segment"""
        if self.is_streaming:
            self.current_segment.append(frame)
            
            # Check if segment is complete
            if len(self.current_segment) >= self.config.fps * self.segment_duration:
                await self._finalize_segment()
                
    async def _finalize_segment(self):
        """Finalize current segment and create new one"""
        if self.current_segment:
            # Save segment as video file
            segment_path = f"{self.output_dir}/segment_{self.segment_counter}.ts"
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(segment_path, fourcc, self.config.fps, self.config.resolution)
            
            for frame in self.current_segment:
                resized = cv2.resize(frame, self.config.resolution)
                out.write(resized)
            out.release()
            
            # Add to playlist
            self.segments.append(segment_path)
            await self._update_playlist()
            
            # Start new segment
            self.current_segment = []
            self.segment_counter += 1
            
    async def _create_playlist(self):
        """Create HLS playlist file"""
        playlist_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:{self.segment_duration}
#EXT-X-MEDIA-SEQUENCE:0
"""
        
        with open(self.playlist_path, 'w') as f:
            f.write(playlist_content)
            
    async def _update_playlist(self):
        """Update HLS playlist with new segments"""
        playlist_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:{self.segment_duration}
#EXT-X-MEDIA-SEQUENCE:0
"""
        
        for segment in self.segments[-10:]:  # Keep last 10 segments
            playlist_content += f"#EXTINF:{self.segment_duration},\n{segment}\n"
            
        playlist_content += "#EXT-X-ENDLIST\n"
        
        with open(self.playlist_path, 'w') as f:
            f.write(playlist_content)

class LiveChatSystem:
    """Live chat system for streams"""
    
    def __init__(self):
        self.chat_rooms = {}
        self.moderators = set()
        self.banned_users = set()
        
    async def create_chat_room(self, room_id: str, max_users: int = 1000):
        """Create a new chat room"""
        self.chat_rooms[room_id] = {
            'users': set(),
            'messages': [],
            'max_users': max_users,
            'created_at': time.time()
        }
        logger.info(f"💬 Chat room created: {room_id}")
        
    async def join_chat(self, room_id: str, user_id: str, username: str):
        """Join a chat room"""
        if room_id not in self.chat_rooms:
            return {'success': False, 'error': 'Room not found'}
            
        if user_id in self.banned_users:
            return {'success': False, 'error': 'User is banned'}
            
        room = self.chat_rooms[room_id]
        if len(room['users']) >= room['max_users']:
            return {'success': False, 'error': 'Room is full'}
            
        room['users'].add(user_id)
        return {'success': True, 'room_id': room_id}
        
    async def send_message(self, room_id: str, user_id: str, message: str):
        """Send message to chat room"""
        if room_id not in self.chat_rooms:
            return {'success': False, 'error': 'Room not found'}
            
        if user_id in self.banned_users:
            return {'success': False, 'error': 'User is banned'}
            
        # Basic message filtering
        filtered_message = self._filter_message(message)
        
        chat_message = {
            'id': f"{room_id}_{int(time.time() * 1000)}",
            'user_id': user_id,
            'message': filtered_message,
            'timestamp': time.time(),
            'type': 'chat'
        }
        
        self.chat_rooms[room_id]['messages'].append(chat_message)
        
        # Keep only last 100 messages
        if len(self.chat_rooms[room_id]['messages']) > 100:
            self.chat_rooms[room_id]['messages'] = self.chat_rooms[room_id]['messages'][-100:]
            
        return {'success': True, 'message_id': chat_message['id']}
        
    def _filter_message(self, message: str) -> str:
        """Filter inappropriate content"""
        # Basic filtering - in production would use more sophisticated methods
        inappropriate_words = ['hack', 'cheat', 'bot', 'aimbot']
        filtered = message
        for word in inappropriate_words:
            filtered = filtered.replace(word, '*' * len(word))
        return filtered
        
    async def moderate_message(self, moderator_id: str, message_id: str, action: str):
        """Moderate a message (delete, warn, ban)"""
        if moderator_id not in self.moderators:
            return {'success': False, 'error': 'Not authorized'}
            
        # Find and moderate message
        for room_id, room in self.chat_rooms.items():
            for msg in room['messages']:
                if msg['id'] == message_id:
                    if action == 'delete':
                        room['messages'].remove(msg)
                    elif action == 'ban':
                        self.banned_users.add(msg['user_id'])
                    return {'success': True}
                    
        return {'success': False, 'error': 'Message not found'}

class RealTimeStreamingSystem:
    """Main real-time streaming system"""
    
    def __init__(self):
        self.webrtc_streamers = {}
        self.rtmp_streamers = {}
        self.hls_streamers = {}
        self.chat_system = LiveChatSystem()
        self.active_streams = {}
        self.stream_callbacks = {}
        
    async def create_stream(self, stream_id: str, config: StreamConfig) -> Dict[str, Any]:
        """Create a new stream"""
        stream_info = {
            'id': stream_id,
            'config': config,
            'created_at': time.time(),
            'viewers': 0,
            'status': 'created'
        }
        
        self.active_streams[stream_id] = stream_info
        
        # Initialize streamers based on protocol
        if config.protocol == 'webrtc':
            self.webrtc_streamers[stream_id] = WebRTCStreamer(config)
        elif config.protocol == 'rtmp':
            self.rtmp_streamers[stream_id] = RTMPStreamer(config)
        elif config.protocol == 'hls':
            self.hls_streamers[stream_id] = HLSStreamer(config)
            
        # Create chat room
        await self.chat_system.create_chat_room(stream_id)
        
        logger.info(f"📡 Stream created: {stream_id} ({config.protocol})")
        return stream_info
        
    async def start_stream(self, stream_id: str, **kwargs):
        """Start streaming"""
        if stream_id not in self.active_streams:
            return {'success': False, 'error': 'Stream not found'}
            
        stream_info = self.active_streams[stream_id]
        config = stream_info['config']
        
        try:
            if config.protocol == 'rtmp':
                rtmp_url = kwargs.get('rtmp_url', f'rtmp://localhost/live/{stream_id}')
                await self.rtmp_streamers[stream_id].start_stream(rtmp_url)
            elif config.protocol == 'hls':
                output_dir = kwargs.get('output_dir', f'./streams/{stream_id}')
                await self.hls_streamers[stream_id].start_stream(output_dir)
                
            stream_info['status'] = 'streaming'
            logger.info(f"🎥 Stream started: {stream_id}")
            return {'success': True}
            
        except Exception as e:
            logger.error(f"❌ Failed to start stream {stream_id}: {e}")
            return {'success': False, 'error': str(e)}
            
    async def send_frame(self, stream_id: str, frame: np.ndarray):
        """Send frame to all active streams"""
        if stream_id not in self.active_streams:
            return
            
        stream_info = self.active_streams[stream_id]
        config = stream_info['config']
        
        try:
            if config.protocol == 'webrtc' and stream_id in self.webrtc_streamers:
                # Send to all connected peers
                for peer_id in self.webrtc_streamers[stream_id].peers:
                    await self.webrtc_streamers[stream_id].send_frame(frame, peer_id)
            elif config.protocol == 'rtmp' and stream_id in self.rtmp_streamers:
                await self.rtmp_streamers[stream_id].send_frame(frame)
            elif config.protocol == 'hls' and stream_id in self.hls_streamers:
                await self.hls_streamers[stream_id].send_frame(frame)
                
        except Exception as e:
            logger.error(f"❌ Failed to send frame to stream {stream_id}: {e}")
            
    async def add_viewer(self, stream_id: str, viewer_id: str, protocol: str = 'webrtc'):
        """Add viewer to stream"""
        if stream_id not in self.active_streams:
            return {'success': False, 'error': 'Stream not found'}
            
        try:
            if protocol == 'webrtc' and stream_id in self.webrtc_streamers:
                offer = await self.webrtc_streamers[stream_id].create_offer(viewer_id)
                self.active_streams[stream_id]['viewers'] += 1
                return {'success': True, 'offer': offer}
            else:
                return {'success': True, 'stream_url': f'http://localhost/streams/{stream_id}/playlist.m3u8'}
                
        except Exception as e:
            logger.error(f"❌ Failed to add viewer to stream {stream_id}: {e}")
            return {'success': False, 'error': str(e)}
            
    async def remove_viewer(self, stream_id: str, viewer_id: str):
        """Remove viewer from stream"""
        if stream_id in self.active_streams:
            self.active_streams[stream_id]['viewers'] = max(0, self.active_streams[stream_id]['viewers'] - 1)
            
    async def stop_stream(self, stream_id: str):
        """Stop streaming"""
        if stream_id not in self.active_streams:
            return {'success': False, 'error': 'Stream not found'}
            
        try:
            if stream_id in self.rtmp_streamers:
                await self.rtmp_streamers[stream_id].stop_stream()
                
            self.active_streams[stream_id]['status'] = 'stopped'
            logger.info(f"🛑 Stream stopped: {stream_id}")
            return {'success': True}
            
        except Exception as e:
            logger.error(f"❌ Failed to stop stream {stream_id}: {e}")
            return {'success': False, 'error': str(e)}
            
    async def get_stream_info(self, stream_id: str) -> Dict[str, Any]:
        """Get stream information"""
        if stream_id in self.active_streams:
            return self.active_streams[stream_id]
        return {'error': 'Stream not found'}
        
    async def list_streams(self) -> List[Dict[str, Any]]:
        """List all active streams"""
        return list(self.active_streams.values())
        
    # Chat system methods
    async def join_chat(self, stream_id: str, user_id: str, username: str):
        """Join stream chat"""
        return await self.chat_system.join_chat(stream_id, user_id, username)
        
    async def send_chat_message(self, stream_id: str, user_id: str, message: str):
        """Send message to stream chat"""
        return await self.chat_system.send_message(stream_id, user_id, message)
        
    async def get_chat_messages(self, stream_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent chat messages"""
        if stream_id in self.chat_system.chat_rooms:
            return self.chat_system.chat_rooms[stream_id]['messages'][-limit:]
        return []
        
    async def shutdown(self):
        """Shutdown streaming system"""
        logger.info("🛑 Shutting down Real-time Streaming System...")
        
        # Stop all active streams
        for stream_id in list(self.active_streams.keys()):
            await self.stop_stream(stream_id) 