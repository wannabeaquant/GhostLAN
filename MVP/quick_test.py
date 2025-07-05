#!/usr/bin/env python3
"""
Quick Test Script for GhostLAN SimWorld
Tests basic functionality without starting the full server
"""

import asyncio
import sys

async def test_basic_imports():
    """Test basic imports"""
    print("🧪 Testing Basic Imports...")
    
    try:
        from duality_scene.simulation import SimulationManager
        print("✅ SimulationManager imported")
        
        from ghostlan_core.anticheat import AntiCheatEngine
        print("✅ AntiCheatEngine imported")
        
        from analytics.pipeline import AnalyticsPipeline
        print("✅ AnalyticsPipeline imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

async def test_object_creation():
    """Test object creation"""
    print("\n🔧 Testing Object Creation...")
    
    try:
        from duality_scene.simulation import SimulationManager
        from ghostlan_core.anticheat import AntiCheatEngine
        from analytics.pipeline import AnalyticsPipeline
        
        sim = SimulationManager()
        print("✅ SimulationManager created")
        
        ac = AntiCheatEngine()
        print("✅ AntiCheatEngine created")
        
        analytics = AnalyticsPipeline()
        print("✅ AnalyticsPipeline created")
        
        return True
    except Exception as e:
        print(f"❌ Object creation failed: {e}")
        return False

async def test_tournament_system():
    """Test tournament system"""
    print("\n🏆 Testing Tournament System...")
    
    try:
        from advanced_tournament.advanced_tournament import AdvancedTournamentManager, TournamentType
        
        tm = AdvancedTournamentManager()
        print("✅ TournamentManager created")
        
        # Test tournament creation
        participants = [
            {"user_id": "player1", "username": "Player1", "rating": 1000},
            {"user_id": "player2", "username": "Player2", "rating": 1100}
        ]
        
        tournament = await tm.create_tournament(
            "test_tournament",
            "Test Tournament",
            TournamentType.SINGLE_ELIMINATION,
            participants
        )
        print("✅ Tournament created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Tournament test failed: {e}")
        return False

async def test_api_endpoints():
    """Test API endpoint imports"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        from api.config import config_router
        print("✅ Config router imported")
        
        from api.export import export_router
        print("✅ Export router imported")
        
        from api.replay import replay_router
        print("✅ Replay router imported")
        
        from api.tournament import tournament_router
        print("✅ Tournament router imported")
        
        return True
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

async def test_advanced_modules():
    """Test advanced module imports"""
    print("\n🚀 Testing Advanced Modules...")
    
    results = {}
    
    # Test ML Pipeline
    try:
        from ml.deep_learning_models import AdvancedMLPipeline
        print("✅ ML Pipeline imported")
        results['ml'] = True
    except ImportError as e:
        print(f"⚠️ ML Pipeline: Missing dependencies ({e})")
        results['ml'] = False
    except Exception as e:
        print(f"❌ ML Pipeline: {e}")
        results['ml'] = False
    
    # Test Streaming System
    try:
        from streaming.real_time_streaming import RealTimeStreamingSystem
        print("✅ Streaming System imported")
        results['streaming'] = True
    except ImportError as e:
        print(f"⚠️ Streaming System: Missing dependencies ({e})")
        results['streaming'] = False
    except Exception as e:
        print(f"❌ Streaming System: {e}")
        results['streaming'] = False
    
    # Test Mobile Backend
    try:
        from mobile.mobile_app import MobileAppBackend
        print("✅ Mobile Backend imported")
        results['mobile'] = True
    except ImportError as e:
        print(f"⚠️ Mobile Backend: Missing dependencies ({e})")
        results['mobile'] = False
    except Exception as e:
        print(f"❌ Mobile Backend: {e}")
        results['mobile'] = False
    
    # Test Cloud Integration
    try:
        from cloud_integration.cloud_services import CloudIntegrationManager
        print("✅ Cloud Integration imported")
        results['cloud'] = True
    except ImportError as e:
        print(f"⚠️ Cloud Integration: Missing dependencies ({e})")
        results['cloud'] = False
    except Exception as e:
        print(f"❌ Cloud Integration: {e}")
        results['cloud'] = False
    
    return results

async def main():
    """Run all tests"""
    print("🎯 GHOSTLAN SIMWORLD - QUICK TEST")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports()),
        ("Object Creation", test_object_creation()),
        ("Tournament System", test_tournament_system()),
        ("API Endpoints", test_api_endpoints()),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = await test_func
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Test advanced modules
    advanced_results = await test_advanced_modules()
    results["Advanced Modules"] = advanced_results
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        if isinstance(result, dict):
            # Advanced modules
            passed_advanced = sum(1 for v in result.values() if v)
            total_advanced = len(result)
            print(f"{test_name}: {passed_advanced}/{total_advanced} modules working")
            passed += passed_advanced
            total += total_advanced - 1  # Adjust for the dict itself
        else:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name}: {status}")
            if result:
                passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed / total >= 0.8:
        print("✅ System is ready for basic operation!")
    elif passed / total >= 0.6:
        print("⚠️ System has some issues but core functionality should work")
    else:
        print("❌ System has significant issues that need to be addressed")
    
    print("\n💡 Next Steps:")
    print("1. Install missing dependencies: pip install dash tensorflow opencv-python qrcode[pil]")
    print("2. Run full test: python test_system.py")
    print("3. Start server: python main.py")

if __name__ == "__main__":
    asyncio.run(main()) 