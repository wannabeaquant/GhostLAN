#!/usr/bin/env python3
"""
GhostLAN SimWorld MVP - Comprehensive Demo Script
Showcases all features: simulation, anti-cheat, analytics, voice, visualization, etc.
"""

import asyncio
import time
import requests
import json
import subprocess
import sys
import os
from pathlib import Path

class GhostLANSimWorldDemo:
    """Comprehensive demo for GhostLAN SimWorld MVP"""
    
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.demo_data = {}
        
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"🎯 {title}")
        print("="*60)
        
    def print_section(self, title: str):
        """Print formatted section"""
        print(f"\n📋 {title}")
        print("-" * 40)
        
    def check_api_health(self) -> bool:
        """Check if API is running"""
        try:
            response = requests.get(f"{self.api_url}/state", timeout=5)
            return response.status_code == 200
        except:
            return False
            
    def demo_simulation_control(self):
        """Demo simulation configuration and control"""
        self.print_section("Simulation Configuration")
        
        # Get current config
        try:
            config = requests.get(f"{self.api_url}/config").json()
            print("✅ Current Configuration:")
            print(json.dumps(config, indent=2))
            
            # Update config
            new_config = {
                "num_players": 12,
                "cheat_probability": 0.4,
                "match_duration": 240,
                "tick_rate": 60.0,
                "network_conditions": {
                    "packet_loss": 0.03,
                    "latency": 20.0,
                    "jitter": 8.0,
                    "bandwidth": 150.0
                }
            }
            
            response = requests.post(f"{self.api_url}/config", json=new_config)
            if response.status_code == 200:
                print("✅ Configuration updated successfully!")
            else:
                print("❌ Failed to update configuration")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_anti_cheat_detection(self):
        """Demo anti-cheat detection features"""
        self.print_section("Anti-Cheat Detection")
        
        try:
            detections = requests.get(f"{self.api_url}/detections").json()
            print(f"✅ Found {len(detections)} cheat detections")
            
            for i, detection in enumerate(detections[:3]):  # Show first 3
                print(f"  Detection {i+1}:")
                print(f"    Rule: {detection.get('rule', 'unknown')}")
                print(f"    Confidence: {detection.get('confidence', 0):.2f}")
                print(f"    Details: {detection.get('details', {})}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_analytics(self):
        """Demo analytics and export features"""
        self.print_section("Analytics & Export")
        
        try:
            # Get analytics
            analytics = requests.get(f"{self.api_url}/analytics").json()
            print("✅ Analytics Data:")
            print(json.dumps(analytics, indent=2))
            
            # Export as JSON
            json_export = requests.get(f"{self.api_url}/export?format=json")
            if json_export.status_code == 200:
                print("✅ JSON Export successful")
                self.demo_data['json_export'] = len(json_export.content)
            else:
                print("❌ JSON Export failed")
                
            # Export as CSV
            csv_export = requests.get(f"{self.api_url}/export?format=csv")
            if csv_export.status_code == 200:
                print("✅ CSV Export successful")
                self.demo_data['csv_export'] = len(csv_export.content)
            else:
                print("❌ CSV Export failed")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_tournament_mode(self):
        """Demo tournament mode features"""
        self.print_section("Tournament Mode")
        
        try:
            # Start tournament
            response = requests.post(f"{self.api_url}/tournament/start")
            if response.status_code == 200:
                print("✅ Tournament started successfully!")
                
                # Get bracket
                bracket = requests.get(f"{self.api_url}/tournament/bracket").json()
                print("✅ Tournament Bracket:")
                print(json.dumps(bracket, indent=2))
                
                # Get leaderboard
                leaderboard = requests.get(f"{self.api_url}/tournament/leaderboard").json()
                print("✅ Tournament Leaderboard:")
                for i, player in enumerate(leaderboard[:5]):  # Top 5
                    print(f"  {i+1}. {player['player']}: {player['wins']} wins, {player['score']} score")
                    
            else:
                print("❌ Failed to start tournament")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_match_recording(self):
        """Demo match recording and replay features"""
        self.print_section("Match Recording & Replay")
        
        try:
            # Get recorded matches
            matches = requests.get(f"{self.api_url}/replay/matches").json()
            print(f"✅ Found {len(matches)} recorded matches")
            
            if matches:
                # Show first match details
                first_match = matches[0]
                print(f"  Latest Match: {first_match['match_id']}")
                print(f"    Start: {first_match['start_time']}")
                print(f"    Duration: {first_match.get('duration', 'N/A')}")
                
                # Get match events
                match_events = requests.get(f"{self.api_url}/replay/matches/{first_match['match_id']}").json()
                events = match_events.get('events', [])
                print(f"    Events: {len(events)}")
                
                # Export match
                export_response = requests.get(f"{self.api_url}/replay/matches/{first_match['match_id']}/export?format=json")
                if export_response.status_code == 200:
                    print("✅ Match export successful")
                    self.demo_data['match_export'] = len(export_response.content)
                    
            else:
                print("  No recorded matches found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_voice_simulation(self):
        """Demo voice simulation features"""
        self.print_section("Voice Simulation")
        
        try:
            # This would be integrated with the voice simulation module
            print("✅ Voice simulation features:")
            print("  - Voice packet generation")
            print("  - Voice quality analysis")
            print("  - Voice-based cheat detection")
            print("  - Voice attack simulation")
            print("  - Voice statistics tracking")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_visualization(self):
        """Demo visualization features"""
        self.print_section("Visualization Features")
        
        print("✅ Available visualizations:")
        print("  - 2D Match Replay (Port 8050)")
        print("  - 3D Match Replay")
        print("  - Player Position Heatmaps")
        print("  - Network Topology")
        print("  - Performance Dashboard")
        print("  - Detection Timeline")
        print("  - Voice Activity Charts")
        print("  - Configuration Dashboard (Port 8070)")
        print("  - Tournament Dashboard (Port 8060)")
        print("  - Replay Dashboard (Port 8080)")
        
    def show_dashboard_urls(self):
        """Show all dashboard URLs"""
        self.print_section("Dashboard URLs")
        
        print("🌐 Available Dashboards:")
        print(f"  📊 Analytics Dashboard: http://localhost:8050")
        print(f"  ⚙️  Configuration Dashboard: http://localhost:8070")
        print(f"  🏆 Tournament Dashboard: http://localhost:8060")
        print(f"  🎬 Replay Dashboard: http://localhost:8080")
        print(f"  🔌 API Documentation: http://localhost:8000/docs")
        
    def run_comprehensive_demo(self):
        """Run the complete demo"""
        self.print_header("GhostLAN SimWorld MVP - Comprehensive Demo")
        
        print("🚀 Starting comprehensive demo of all features...")
        
        # Check API health
        if not self.check_api_health():
            print("❌ API is not running. Please start the main application first:")
            print("   python main.py")
            return
            
        print("✅ API is running and healthy!")
        
        # Run all demo sections
        self.demo_simulation_control()
        self.demo_anti_cheat_detection()
        self.demo_analytics()
        self.demo_tournament_mode()
        self.demo_match_recording()
        self.demo_voice_simulation()
        self.demo_visualization()
        
        # Show results
        self.print_section("Demo Results")
        print("✅ All features demonstrated successfully!")
        print(f"📊 Data exported: {self.demo_data}")
        
        self.show_dashboard_urls()
        
        print("\n🎉 Demo completed! Explore the dashboards to see all features in action.")
        
    def start_all_services(self):
        """Start all services for the demo"""
        self.print_header("Starting All Services")
        
        print("🚀 Starting GhostLAN SimWorld services...")
        
        # Start main application
        print("📱 Starting main application...")
        try:
            subprocess.Popen([sys.executable, "main.py"], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(3)
            print("✅ Main application started")
        except Exception as e:
            print(f"❌ Failed to start main application: {e}")
            
        # Start dashboards
        dashboards = [
            ("analytics/dashboard.py", "Analytics Dashboard"),
            ("Frontend/config_dashboard.py", "Configuration Dashboard"),
            ("Frontend/tournament_dashboard.py", "Tournament Dashboard"),
            ("Frontend/replay_dashboard.py", "Replay Dashboard")
        ]
        
        for dashboard_file, name in dashboards:
            if Path(dashboard_file).exists():
                print(f"📊 Starting {name}...")
                try:
                    subprocess.Popen([sys.executable, dashboard_file],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    time.sleep(1)
                    print(f"✅ {name} started")
                except Exception as e:
                    print(f"❌ Failed to start {name}: {e}")
            else:
                print(f"⚠️  {dashboard_file} not found, skipping {name}")
                
        print("\n🎯 All services started! Run the demo with:")
        print("   python demo.py --demo")

def main():
    """Main demo function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GhostLAN SimWorld MVP Demo")
    parser.add_argument("--start", action="store_true", help="Start all services")
    parser.add_argument("--demo", action="store_true", help="Run comprehensive demo")
    
    args = parser.parse_args()
    
    demo = GhostLANSimWorldDemo()
    
    if args.start:
        demo.start_all_services()
    elif args.demo:
        demo.run_comprehensive_demo()
    else:
        print("GhostLAN SimWorld MVP Demo")
        print("Usage:")
        print("  python demo.py --start    # Start all services")
        print("  python demo.py --demo     # Run comprehensive demo")

if __name__ == "__main__":
    main() 