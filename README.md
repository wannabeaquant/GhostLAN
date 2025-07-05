# GhostLAN SimWorld - Powered by Duality AI

GhostLAN SimWorld is a comprehensive digital twin simulation platform for offline eSports anti-cheat testing, powered by Duality AI. This advanced platform creates realistic LAN environments with AI agents exhibiting both normal and cheat-prone behaviors, enabling thorough testing of anti-cheat systems, analytics, match recording, and tournament management before live events.

## 🎯 **Core Features**

- **🤖 Duality AI Integration**: Advanced AI agents with realistic gaming behaviors
- **🛡️ Anti-Cheat Testing**: Pre-tournament validation of anti-cheat systems
- **📊 Offline Analytics**: Comprehensive performance analysis and reporting
- **🎬 Match Recording**: Full match capture and replay functionality
- **🏆 Tournament Management**: Complete tournament platform with advanced features
- **📱 Mobile Integration**: iOS/Android app support for tournament management
- **📡 Real-time Streaming**: Live tournament broadcasting capabilities
- **☁️ Cloud Deployment**: Scalable cloud infrastructure support

## 🏗️ **Architecture**

```
MVP/
├── duality_scene/          # Duality AI simulation environment
├── ghostlan_core/          # Core anti-cheat engine
├── analytics/              # Analytics and reporting system
├── api/                    # REST API endpoints
├── streaming/              # Real-time streaming system
├── mobile/                 # Mobile app backend
├── cloud_integration/      # Cloud deployment support
├── advanced_tournament/    # Advanced tournament features
├── Frontend/               # Web dashboards
└── main.py                 # Main application entry point
```

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8+
- ✅ **Duality AI API key**: Already configured in `.env` file

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MVP
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **✅ Duality AI is already configured!**
   - API key is set in `.env` file
   - Platform runs in enhanced API mode
   - No additional setup required

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the platform**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

6. **Test configuration**
   ```bash
   python test_config.py
   ```

## 🤖 **Duality AI Integration**

### **✅ API Mode (Currently Active)**
Your platform is configured with a Duality AI API key and running in enhanced API mode with:
- **Enhanced AI Capabilities**: Cloud-based intelligence
- **Advanced Behavioral Patterns**: Sophisticated agent behaviors
- **Real-time Processing**: Fast response times
- **Scalable Infrastructure**: Cloud-powered performance

### **Local Mode (Fallback)**
If no API key is configured, the platform runs in local simulation mode with:
- **Local Simulation**: Intelligent AI agents
- **Realistic Gaming Behaviors**: Mimics human players
- **Offline Operation**: No internet required

### **Features**
- **Intelligent Agents**: 10 AI agents with realistic gaming behaviors
- **Configurable Cheating**: 4 agents with configurable cheating behaviors
- **Digital Twin Environment**: Realistic LAN café simulation
- **Dynamic Interactions**: Agents respond to environment and other players

## 🛡️ **Anti-Cheat Testing**

### **Rule-Based Detection**
- **Movement Analysis**: Detects impossible movements and teleportation
- **Aim Analysis**: Identifies suspicious aiming patterns
- **Timing Analysis**: Detects inhuman reaction times
- **Behavior Analysis**: Monitors for unusual player behaviors

### **Testing Scenarios**
- **Normal Play**: 6 agents with realistic gaming behaviors
- **Cheat Testing**: 4 agents with configurable cheating patterns
- **Mixed Scenarios**: Realistic tournament environments
- **Edge Cases**: Extreme cheating scenarios for system validation

## 📊 **Analytics & Reporting**

### **Real-time Analytics**
- **Performance Metrics**: FPS, latency, accuracy tracking
- **Behavior Analysis**: Player movement and interaction patterns
- **Cheat Detection**: Real-time anti-cheat alerts
- **Tournament Stats**: Comprehensive tournament analytics

### **Offline Analysis**
- **Match Replays**: Full match recording and playback
- **Performance Reports**: Detailed performance analysis
- **Trend Analysis**: Long-term performance trends
- **Export Capabilities**: Data export in multiple formats

## 🏆 **Tournament Management**

### **Advanced Features**
- **Tournament Creation**: Easy tournament setup and configuration
- **Player Management**: Comprehensive player registration and management
- **Match Scheduling**: Automated match scheduling and management
- **Results Tracking**: Real-time results and standings
- **Mobile Integration**: iOS/Android app for tournament management

## 📱 **Mobile Integration**

### **Mobile App Features**
- **Tournament Management**: Create and manage tournaments
- **Player Registration**: Easy player registration and check-in
- **Match Updates**: Real-time match status and results
- **Notifications**: Push notifications for important events
- **Offline Support**: Works without internet connection

## 📡 **Real-time Streaming**

### **Streaming Capabilities**
- **Live Broadcasting**: Real-time tournament streaming
- **Multi-platform**: Support for multiple streaming platforms
- **Quality Control**: Adaptive quality based on network conditions
- **Recording**: Automatic stream recording for later analysis

## ☁️ **Cloud Deployment**

### **Cloud Features**
- **Scalable Infrastructure**: Auto-scaling based on demand
- **Multi-region**: Global deployment capabilities
- **Monitoring**: Comprehensive cloud monitoring and alerting
- **Backup**: Automated data backup and recovery

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Duality AI Configuration (✅ Already configured)
DUALITY_AI_API_KEY=your-api-key-here
DUALITY_AI_API_URL=https://api.duality.ai

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///ghostlan.db

# Cloud Configuration
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

### **Configuration Files**
- `.env` - ✅ Contains your Duality AI API key (already configured)
- `config.env` - Template file for reference
- `duality_ai_config.py` - Configuration management

## 📚 **API Documentation**

### **Core Endpoints**
- `GET /` - Platform overview
- `GET /health` - Health check
- `GET /api/v1/status` - API status

### **Tournament Endpoints**
- `GET /api/v1/tournament` - Tournament management
- `POST /api/v1/tournament/create` - Create tournament
- `GET /api/v1/tournament/{id}` - Get tournament details

### **Analytics Endpoints**
- `GET /api/v1/analytics` - Analytics data
- `GET /api/v1/export` - Data export
- `GET /api/v1/replay` - Match replay

### **Mobile Endpoints**
- `POST /api/v1/mobile/auth` - Mobile authentication
- `GET /api/v1/mobile/tournaments` - Mobile tournament data

## 🧪 **Testing**

### **Run Tests**
```bash
# Test configuration
python test_config.py

# Run comprehensive demo
python demo_final.py

# Run all tests
python test_system.py

# Run specific test modules
python -m pytest tests/
```

### **Test Coverage**
- **Unit Tests**: Individual component testing
- **Integration Tests**: System integration testing
- **Performance Tests**: Load and stress testing
- **Security Tests**: Security vulnerability testing

## 🚀 **Deployment**

### **Local Development**
```bash
python main.py
```

### **Production Deployment**
```bash
# Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Using Docker
docker build -t ghostlan-simworld .
docker run -p 8000:8000 ghostlan-simworld
```

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 **Support**

For support and questions:
- **Email**: support@ghostlan.com
- **Documentation**: https://docs.ghostlan.com
- **Issues**: GitHub Issues

---

**Powered by Duality AI** 🤖

*Revolutionizing eSports anti-cheat testing with intelligent digital twin simulation* 
