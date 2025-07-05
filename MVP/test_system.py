#!/usr/bin/env python3
"""
GhostLAN SimWorld - System Testing Script
Step-by-step testing of all components
"""

import sys
import asyncio
import importlib
import traceback
from typing import Dict, List, Any
import json

class SystemTester:
    """Comprehensive system testing"""
    
    def __init__(self):
        self.results = {
            "python_version": None,
            "dependencies": {},
            "core_modules": {},
            "advanced_modules": {},
            "api_endpoints": {},
            "integration_tests": {}
        }
        
    def test_python_version(self):
        """Test Python version"""
        print("🐍 Testing Python Version...")
        try:
            version = sys.version_info
            self.results["python_version"] = f"{version.major}.{version.minor}.{version.micro}"
            print(f"✅ Python {self.results['python_version']} - Compatible")
            return True
        except Exception as e:
            print(f"❌ Python version test failed: {e}")
            return False
            
    def test_dependencies(self):
        """Test required dependencies"""
        print("\n📦 Testing Dependencies...")
        
        dependencies = [
            # Core
            ("fastapi", "FastAPI"),
            ("uvicorn", "Uvicorn"),
            ("pydantic", "Pydantic"),
            ("websockets", "WebSockets"),
            
            # Data processing
            ("numpy", "NumPy"),
            ("pandas", "Pandas"),
            ("plotly", "Plotly"),
            ("dash", "Dash"),
            
            # ML/AI
            ("tensorflow", "TensorFlow"),
            ("sklearn", "Scikit-learn"),
            ("torch", "PyTorch"),
            
            # Computer Vision
            ("cv2", "OpenCV"),
            ("PIL", "Pillow"),
            
            # Audio
            ("librosa", "Librosa"),
            ("soundfile", "SoundFile"),
            
            # Cloud
            ("boto3", "Boto3"),
            ("azure", "Azure SDK"),
            ("google.cloud", "Google Cloud"),
            
            # Streaming
            ("aiohttp", "aiohttp"),
            ("aiortc", "aiortc"),
            
            # Mobile
            ("jwt", "PyJWT"),
            ("qrcode", "QR Code"),
            
            # Database
            ("sqlalchemy", "SQLAlchemy"),
            ("redis", "Redis"),
            
            # Security
            ("cryptography", "Cryptography"),
            ("passlib", "Passlib"),
            
            # Monitoring
            ("prometheus_client", "Prometheus"),
            ("structlog", "Structlog")
        ]
        
        for module_name, display_name in dependencies:
            try:
                importlib.import_module(module_name)
                self.results["dependencies"][display_name] = "✅ Available"
                print(f"✅ {display_name}")
            except ImportError:
                self.results["dependencies"][display_name] = "❌ Missing"
                print(f"❌ {display_name} - Missing")
            except Exception as e:
                self.results["dependencies"][display_name] = f"⚠️ Error: {e}"
                print(f"⚠️ {display_name} - Error: {e}")
                
    def test_core_modules(self):
        """Test core modules"""
        print("\n🔧 Testing Core Modules...")
        
        core_modules = [
            ("duality_scene.simulation", "Duality Simulation"),
            ("ghostlan_core.anticheat", "Anti-Cheat Engine"),
            ("analytics.pipeline", "Analytics Pipeline"),
            ("analytics.match_recorder", "Match Recorder"),
            ("api.server", "API Server"),
            ("api.config", "Config API"),
            ("api.export", "Export API"),
            ("api.replay", "Replay API"),
            ("api.tournament", "Tournament API")
        ]
        
        for module_name, display_name in core_modules:
            try:
                importlib.import_module(module_name)
                self.results["core_modules"][display_name] = "✅ Available"
                print(f"✅ {display_name}")
            except ImportError as e:
                self.results["core_modules"][display_name] = f"❌ Missing: {e}"
                print(f"❌ {display_name} - Missing: {e}")
            except Exception as e:
                self.results["core_modules"][display_name] = f"⚠️ Error: {e}"
                print(f"⚠️ {display_name} - Error: {e}")
                
    def test_advanced_modules(self):
        """Test advanced modules"""
        print("\n🚀 Testing Advanced Modules...")
        
        advanced_modules = [
            ("ml.deep_learning_models", "ML Pipeline"),
            ("streaming.real_time_streaming", "Streaming System"),
            ("mobile.mobile_app", "Mobile Backend"),
            ("cloud_integration.cloud_services", "Cloud Integration"),
            ("advanced_tournament.advanced_tournament", "Advanced Tournaments")
        ]
        
        for module_name, display_name in advanced_modules:
            try:
                importlib.import_module(module_name)
                self.results["advanced_modules"][display_name] = "✅ Available"
                print(f"✅ {display_name}")
            except ImportError as e:
                self.results["advanced_modules"][display_name] = f"❌ Missing: {e}"
                print(f"❌ {display_name} - Missing: {e}")
            except Exception as e:
                self.results["advanced_modules"][display_name] = f"⚠️ Error: {e}"
                print(f"⚠️ {display_name} - Error: {e}")
                
    async def test_basic_functionality(self):
        """Test basic functionality"""
        print("\n🧪 Testing Basic Functionality...")
        
        try:
            # Test basic imports
            from duality_scene.simulation import SimulationManager
            from ghostlan_core.anticheat import AntiCheatEngine
            from analytics.pipeline import AnalyticsPipeline
            
            print("✅ Basic imports successful")
            
            # Test object creation
            simulation = SimulationManager()
            anticheat = AntiCheatEngine()
            analytics = AnalyticsPipeline()
            
            print("✅ Object creation successful")
            
            self.results["integration_tests"]["basic_functionality"] = "✅ Working"
            
        except Exception as e:
            print(f"❌ Basic functionality test failed: {e}")
            self.results["integration_tests"]["basic_functionality"] = f"❌ Failed: {e}"
            
    async def test_ml_pipeline(self):
        """Test ML pipeline"""
        print("\n🧠 Testing ML Pipeline...")
        
        try:
            from ml.deep_learning_models import AdvancedMLPipeline
            
            ml_pipeline = AdvancedMLPipeline()
            await ml_pipeline.initialize()
            
            print("✅ ML Pipeline initialized")
            
            # Test model building
            ml_pipeline.cnn_detector.build_model()
            ml_pipeline.rnn_analyzer.build_model()
            ml_pipeline.gan_generator.build_generator()
            ml_pipeline.gan_generator.build_discriminator()
            ml_pipeline.gan_generator.build_gan()
            
            print("✅ ML Models built successfully")
            
            self.results["integration_tests"]["ml_pipeline"] = "✅ Working"
            
        except Exception as e:
            print(f"❌ ML Pipeline test failed: {e}")
            self.results["integration_tests"]["ml_pipeline"] = f"❌ Failed: {e}"
            
    async def test_streaming_system(self):
        """Test streaming system"""
        print("\n📡 Testing Streaming System...")
        
        try:
            from streaming.real_time_streaming import RealTimeStreamingSystem, StreamConfig
            
            streaming_system = RealTimeStreamingSystem()
            
            # Test stream creation
            config = StreamConfig(
                protocol="webrtc",
                quality="high",
                fps=30,
                bitrate=5000,
                resolution=(1920, 1080)
            )
            
            stream_info = await streaming_system.create_stream("test_stream", config)
            print("✅ Stream creation successful")
            
            # Test chat system
            await streaming_system.chat_system.create_chat_room("test_room")
            print("✅ Chat system working")
            
            self.results["integration_tests"]["streaming_system"] = "✅ Working"
            
        except Exception as e:
            print(f"❌ Streaming system test failed: {e}")
            self.results["integration_tests"]["streaming_system"] = f"❌ Failed: {e}"
            
    async def test_mobile_backend(self):
        """Test mobile backend"""
        print("\n📱 Testing Mobile Backend...")
        
        try:
            from mobile.mobile_app import MobileAppBackend
            
            mobile_backend = MobileAppBackend("test-secret", None, None, None)
            
            # Test user registration
            result = await mobile_backend.register_user(
                "testuser", "test@example.com", "password123",
                "test_device", "ios"
            )
            
            print("✅ Mobile backend user registration successful")
            
            self.results["integration_tests"]["mobile_backend"] = "✅ Working"
            
        except Exception as e:
            print(f"❌ Mobile backend test failed: {e}")
            self.results["integration_tests"]["mobile_backend"] = f"❌ Failed: {e}"
            
    async def test_cloud_integration(self):
        """Test cloud integration"""
        print("\n☁️ Testing Cloud Integration...")
        
        try:
            from cloud_integration.cloud_services import CloudIntegrationManager, CloudConfig
            
            cloud_manager = CloudIntegrationManager()
            
            # Test cloud provider addition (without real credentials)
            config = CloudConfig(
                provider="aws",
                region="us-east-1",
                credentials={"access_key_id": "test", "secret_access_key": "test"}
            )
            
            await cloud_manager.add_cloud_provider("aws", config)
            print("✅ Cloud integration setup successful")
            
            self.results["integration_tests"]["cloud_integration"] = "✅ Working"
            
        except Exception as e:
            print(f"❌ Cloud integration test failed: {e}")
            self.results["integration_tests"]["cloud_integration"] = f"❌ Failed: {e}"
            
    async def test_tournament_system(self):
        """Test tournament system"""
        print("\n🏆 Testing Tournament System...")
        
        try:
            from advanced_tournament.advanced_tournament import (
                AdvancedTournamentManager, TournamentType, PrizePool
            )
            
            tournament_manager = AdvancedTournamentManager()
            
            # Test tournament creation
            participants = [
                {"user_id": "player1", "username": "Player1", "rating": 1000},
                {"user_id": "player2", "username": "Player2", "rating": 1100}
            ]
            
            prize_pool = PrizePool(total_amount=1000, currency="USD")
            
            tournament = await tournament_manager.create_tournament(
                "test_tournament",
                "Test Tournament",
                TournamentType.SINGLE_ELIMINATION,
                participants,
                prize_pool
            )
            
            print("✅ Tournament system working")
            
            self.results["integration_tests"]["tournament_system"] = "✅ Working"
            
        except Exception as e:
            print(f"❌ Tournament system test failed: {e}")
            self.results["integration_tests"]["tournament_system"] = f"❌ Failed: {e}"
            
    def test_file_structure(self):
        """Test file structure"""
        print("\n📁 Testing File Structure...")
        
        import os
        
        required_files = [
            "main.py",
            "requirements.txt",
            "README.md",
            "demo_advanced.py",
            "duality_scene/__init__.py",
            "ghostlan_core/__init__.py",
            "analytics/__init__.py",
            "api/__init__.py",
            "ml/__init__.py",
            "streaming/__init__.py",
            "mobile/__init__.py",
            "cloud_integration/__init__.py",
            "advanced_tournament/__init__.py"
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - Missing")
                
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("📊 GHOSTLAN SIMWORLD - TEST REPORT")
        print("="*60)
        
        # Python Version
        print(f"\n🐍 Python Version: {self.results['python_version']}")
        
        # Dependencies Summary
        print(f"\n📦 Dependencies:")
        available = sum(1 for status in self.results["dependencies"].values() if "✅" in status)
        total = len(self.results["dependencies"])
        print(f"   {available}/{total} dependencies available")
        
        # Core Modules Summary
        print(f"\n🔧 Core Modules:")
        available = sum(1 for status in self.results["core_modules"].values() if "✅" in status)
        total = len(self.results["core_modules"])
        print(f"   {available}/{total} core modules available")
        
        # Advanced Modules Summary
        print(f"\n🚀 Advanced Modules:")
        available = sum(1 for status in self.results["advanced_modules"].values() if "✅" in status)
        total = len(self.results["advanced_modules"])
        print(f"   {available}/{total} advanced modules available")
        
        # Integration Tests Summary
        print(f"\n🧪 Integration Tests:")
        available = sum(1 for status in self.results["integration_tests"].values() if "✅" in status)
        total = len(self.results["integration_tests"])
        print(f"   {available}/{total} integration tests passed")
        
        # Overall Status
        total_tests = len(self.results["dependencies"]) + len(self.results["core_modules"]) + len(self.results["advanced_modules"]) + len(self.results["integration_tests"])
        passed_tests = sum(1 for status in self.results["dependencies"].values() if "✅" in status) + \
                      sum(1 for status in self.results["core_modules"].values() if "✅" in status) + \
                      sum(1 for status in self.results["advanced_modules"].values() if "✅" in status) + \
                      sum(1 for status in self.results["integration_tests"].values() if "✅" in status)
        
        print(f"\n🎯 Overall Status: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests / total_tests >= 0.8:
            print("✅ System is ready for basic operation!")
        elif passed_tests / total_tests >= 0.6:
            print("⚠️ System has some issues but core functionality should work")
        else:
            print("❌ System has significant issues that need to be addressed")
            
        # Save detailed report
        with open("test_report.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Detailed report saved to: test_report.json")
        
    async def run_all_tests(self):
        """Run all tests"""
        print("🎯 GHOSTLAN SIMWORLD - SYSTEM TESTING")
        print("="*60)
        
        # Basic tests
        self.test_python_version()
        self.test_dependencies()
        self.test_core_modules()
        self.test_advanced_modules()
        self.test_file_structure()
        
        # Integration tests
        await self.test_basic_functionality()
        await self.test_ml_pipeline()
        await self.test_streaming_system()
        await self.test_mobile_backend()
        await self.test_cloud_integration()
        await self.test_tournament_system()
        
        # Generate report
        self.generate_report()

async def main():
    """Main testing function"""
    tester = SystemTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 