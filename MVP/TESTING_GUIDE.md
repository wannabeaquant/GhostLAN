# GhostLAN SimWorld - Step-by-Step Testing Guide

## 📊 Current Status (Based on Test Results)

**Overall: 30/48 tests passed (62.5%)**

### ✅ **What Works Right Now**
- Python 3.13.2 ✅
- Core API framework (FastAPI, Uvicorn) ✅
- Basic data processing (NumPy, Pandas, Plotly) ✅
- Core modules (simulation, anti-cheat, analytics) ✅
- Tournament system ✅
- Cloud services (AWS, Google Cloud) ✅
- Security libraries ✅

### ⚠️ **What Needs Dependencies**
- Machine Learning (TensorFlow missing)
- Computer Vision (OpenCV missing)
- Mobile features (QR Code missing)
- Audio processing (Librosa, SoundFile missing)
- Streaming (aiortc missing)
- Azure integration (Azure SDK missing)

### ❌ **What Needs Fixes**
- Some import errors (now fixed)
- Missing `__init__.py` files (now fixed)

---

## 🚀 **STEP-BY-STEP TESTING**

### **STEP 1: Quick Start (What Works Now)**

#### 1.1 Test Basic Server
```bash
# Start the server
python main.py
```

**Expected Result**: Server starts on http://localhost:8000
**Test**: Visit http://localhost:8000/health

#### 1.2 Test Core API Endpoints
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint  
curl http://localhost:8000/

# Test API status
curl http://localhost:8000/api/v1/status
```

#### 1.3 Test Tournament System
```bash
# Run tournament test
python -c "
import asyncio
from advanced_tournament.advanced_tournament import AdvancedTournamentManager, TournamentType
async def test():
    tm = AdvancedTournamentManager()
    print('✅ Tournament system working')
asyncio.run(test())
"
```

---

### **STEP 2: Install Missing Dependencies**

#### 2.1 Essential Dependencies (Recommended)
```bash
# Install core missing dependencies
pip install dash tensorflow opencv-python qrcode[pil] structlog
```

#### 2.2 Optional Dependencies
```bash
# Audio processing (for voice analysis)
pip install librosa soundfile

# Advanced streaming
pip install aiortc ffmpeg-python

# Azure cloud integration
pip install azure-mgmt-compute azure-mgmt-network azure-monitor
```

#### 2.3 Install Everything
```bash
# Install all dependencies from requirements.txt
pip install -r requirements.txt
```

---

### **STEP 3: Test Advanced Features**

#### 3.1 Machine Learning Pipeline
```bash
# Test ML pipeline
python -c "
import asyncio
from ml.deep_learning_models import AdvancedMLPipeline
async def test():
    ml = AdvancedMLPipeline()
    await ml.initialize()
    print('✅ ML Pipeline working')
asyncio.run(test())
"
```

#### 3.2 Streaming System
```bash
# Test streaming
python -c "
import asyncio
from streaming.real_time_streaming import RealTimeStreamingSystem
async def test():
    streaming = RealTimeStreamingSystem()
    print('✅ Streaming system working')
asyncio.run(test())
"
```

#### 3.3 Mobile Backend
```bash
# Test mobile backend
python -c "
import asyncio
from mobile.mobile_app import MobileAppBackend
async def test():
    mobile = MobileAppBackend('test-key', None, None, None)
    print('✅ Mobile backend working')
asyncio.run(test())
"
```

---

### **STEP 4: Run Comprehensive Tests**

#### 4.1 Run Full Test Suite
```bash
# Run the comprehensive test
python test_system.py
```

#### 4.2 Check Test Report
```bash
# View detailed results
cat test_report.json
```

---

### **STEP 5: Test Individual Components**

#### 5.1 Test Simulation
```bash
# Test basic simulation
python -c "
import asyncio
from duality_scene.simulation import SimulationManager
async def test():
    sim = SimulationManager()
    await sim.initialize()
    print('✅ Simulation working')
asyncio.run(test())
"
```

#### 5.2 Test Anti-Cheat
```bash
# Test anti-cheat engine
python -c "
import asyncio
from ghostlan_core.anticheat import GhostLANAntiCheat
async def test():
    ac = GhostLANAntiCheat()
    await ac.initialize()
    print('✅ Anti-cheat working')
asyncio.run(test())
"
```

#### 5.3 Test Analytics
```bash
# Test analytics pipeline
python -c "
import asyncio
from analytics.pipeline import AnalyticsPipeline
async def test():
    analytics = AnalyticsPipeline()
    await analytics.initialize()
    print('✅ Analytics working')
asyncio.run(test())
"
```

---

### **STEP 6: Test API Endpoints**

#### 6.1 Start Server
```bash
python main.py
```

#### 6.2 Test Endpoints
```bash
# Health check
curl http://localhost:8000/health

# API status
curl http://localhost:8000/api/v1/status

# Configuration
curl http://localhost:8000/api/v1/config

# Export
curl http://localhost:8000/api/v1/export

# Tournament
curl http://localhost:8000/api/v1/tournament
```

#### 6.3 Test WebSocket
```bash
# Use a WebSocket client or browser
# Connect to: ws://localhost:8000/ws
```

---

### **STEP 7: Test Advanced Features**

#### 7.1 Machine Learning (After installing TensorFlow)
```bash
# Test ML predictions
python -c "
import numpy as np
from ml.deep_learning_models import CNNCheatDetector
detector = CNNCheatDetector()
detector.build_model()
data = np.random.rand(64, 64, 3)
result = detector.predict_cheat(data)
print('✅ ML prediction:', result)
"
```

#### 7.2 Streaming (After installing OpenCV)
```bash
# Test streaming
python -c "
import asyncio
import numpy as np
from streaming.real_time_streaming import RealTimeStreamingSystem, StreamConfig
async def test():
    streaming = RealTimeStreamingSystem()
    config = StreamConfig(protocol='webrtc', quality='high')
    await streaming.create_stream('test', config)
    print('✅ Streaming working')
asyncio.run(test())
"
```

#### 7.3 Mobile API (After installing QR Code)
```bash
# Test mobile endpoints
curl -X POST http://localhost:8000/api/v1/mobile/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test","device_id":"test","platform":"ios"}'
```

---

### **STEP 8: Run Demo**

#### 8.1 Basic Demo
```bash
# Run the basic demo
python demo.py
```

#### 8.2 Advanced Demo (After installing dependencies)
```bash
# Run the advanced demo
python demo_advanced.py
```

---

## 🔧 **TROUBLESHOOTING**

### **Common Issues**

#### Issue 1: Import Errors
```bash
# Fix: Install missing dependencies
pip install <missing-package>
```

#### Issue 2: Module Not Found
```bash
# Fix: Check if __init__.py files exist
ls -la */__init__.py
```

#### Issue 3: TensorFlow Issues
```bash
# Fix: Install TensorFlow for your platform
pip install tensorflow
# or for CPU only
pip install tensorflow-cpu
```

#### Issue 4: OpenCV Issues
```bash
# Fix: Install OpenCV
pip install opencv-python
```

#### Issue 5: Port Already in Use
```bash
# Fix: Change port or kill existing process
python main.py --port 8001
# or
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 📊 **EXPECTED RESULTS**

### **After Step 1 (Basic)**
- ✅ Server starts on port 8000
- ✅ Health endpoint responds
- ✅ Basic API endpoints work
- ✅ Tournament system functional

### **After Step 2 (Dependencies)**
- ✅ All core dependencies installed
- ✅ ML pipeline available
- ✅ Streaming system available
- ✅ Mobile features available

### **After Step 3 (Advanced)**
- ✅ ML predictions working
- ✅ Real-time streaming functional
- ✅ Mobile API endpoints responding
- ✅ Cloud integration available

### **After Step 4 (Full System)**
- ✅ All tests passing
- ✅ Complete functionality available
- ✅ Ready for production use

---

## 🎯 **SUCCESS CRITERIA**

### **Minimum Viable System**
- ✅ Server starts and responds
- ✅ Core API endpoints work
- ✅ Basic simulation runs
- ✅ Tournament system functional

### **Full Feature System**
- ✅ All dependencies installed
- ✅ ML pipeline operational
- ✅ Streaming system working
- ✅ Mobile API functional
- ✅ Cloud integration ready
- ✅ All tests passing

---

## 📞 **GETTING HELP**

### **If Tests Fail**
1. Check the error messages in `test_report.json`
2. Install missing dependencies
3. Check Python version compatibility
4. Verify file permissions

### **If Server Won't Start**
1. Check if port 8000 is available
2. Verify all dependencies are installed
3. Check Python environment
4. Review error logs

### **If Features Don't Work**
1. Install specific missing dependencies
2. Check import statements
3. Verify module structure
4. Test individual components

---

**🎮 Happy Testing! The system should be fully functional once all dependencies are installed.** 