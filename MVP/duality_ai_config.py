#!/usr/bin/env python3
"""
Duality AI Configuration for GhostLAN
Handles API key and integration settings
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file (or config.env as fallback)
load_dotenv()  # Try .env first
load_dotenv("config.env")  # Fallback to config.env

logger = logging.getLogger(__name__)

class DualityAIConfig:
    """Configuration for Duality AI integration"""
    
    def __init__(self):
        self.api_key = os.getenv("DUALITY_AI_API_KEY")
        self.api_url = os.getenv("DUALITY_AI_API_URL", "https://api.duality.ai")
        self.enabled = self.api_key is not None and self.api_key != "your-duality-ai-api-key-here"
        
    def is_configured(self) -> bool:
        """Check if Duality AI is properly configured"""
        return self.enabled and self.api_key is not None and self.api_key != "your-duality-ai-api-key-here"
    
    def get_api_key(self) -> Optional[str]:
        """Get Duality AI API key"""
        return self.api_key if self.api_key != "your-duality-ai-api-key-here" else None
    
    def get_api_url(self) -> str:
        """Get Duality AI API URL"""
        return self.api_url
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for Duality AI API requests"""
        if not self.api_key or self.api_key == "your-duality-ai-api-key-here":
            return {}
        
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "GhostLAN-SimWorld/2.0.0"
        }
    
    def log_status(self):
        """Log Duality AI configuration status"""
        if self.enabled:
            logger.info("✅ Duality AI is configured and enabled")
            logger.info(f"   API URL: {self.api_url}")
            logger.info("   API Key: [CONFIGURED]")
        else:
            logger.warning("⚠️ Duality AI is not configured")
            logger.info("   To enable Duality AI, add DUALITY_AI_API_KEY to .env file")
            logger.info("   Example: DUALITY_AI_API_KEY=your-actual-api-key")
            logger.info("   Or copy config.env to .env and update the API key")

# Global configuration instance
duality_config = DualityAIConfig()

def get_duality_config() -> DualityAIConfig:
    """Get Duality AI configuration"""
    return duality_config

def setup_duality_ai():
    """Setup Duality AI integration"""
    duality_config.log_status()
    
    if duality_config.is_configured():
        logger.info("🚀 Duality AI integration ready")
        return True
    else:
        logger.info("🔄 Running in local simulation mode (no Duality AI API)")
        return False

if __name__ == "__main__":
    # Test configuration
    setup_duality_ai()
    
    if duality_config.is_configured():
        print("✅ Duality AI is properly configured")
        print(f"   API URL: {duality_config.get_api_url()}")
        print("   API Key: [CONFIGURED]")
    else:
        print("⚠️ Duality AI is not configured")
        print("   Add DUALITY_AI_API_KEY to .env file to enable")
        print("   Example: DUALITY_AI_API_KEY=your-actual-api-key")
        print("   Or copy config.env to .env and update the API key") 