# GhostLAN SimWorld - Setup Guide
## Duality AI Configuration

### 🎯 **Current Status: ✅ CONFIGURED**

Your GhostLAN SimWorld platform is **already configured** with a Duality AI API key and ready to run in **API Mode**!

### 🔧 **Environment Configuration**

#### **Current Setup:**
- ✅ **Duality AI API Key**: Configured in `.env` file
- ✅ **API Mode**: Enabled (enhanced AI capabilities)
- ✅ **Environment Variables**: Loaded automatically

#### **Files:**
- `.env` - Contains your Duality AI API key (already configured)
- `config.env` - Template file for reference
- `duality_ai_config.py` - Configuration management

### 🚀 **Quick Start**

#### **1. Verify Configuration:**
```bash
python test_config.py
```

**Expected Output:**
```
🔧 Duality AI Configuration Test
========================================
API Key: [YOUR-API-KEY]
API URL: https://api.duality.ai
Is Configured: True
Enabled: True
✅ Duality AI is properly configured!
```

#### **2. Run the Application:**
```bash
python main.py
```

**Expected Output:**
```
🤖 Initializing Duality AI Simulation Environment (API Mode)...
✅ Duality AI Simulation initialized with 10 intelligent agents
```

#### **3. Test API Endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Platform overview
curl http://localhost:8000/
```

### 🤖 **Duality AI Modes**

#### **API Mode (Current - Enhanced):**
- ✅ **Duality AI API Key**: Configured
- ✅ **Enhanced AI Capabilities**: Available
- ✅ **Cloud-based Intelligence**: Active
- ✅ **Advanced Behavioral Patterns**: Enabled

#### **Local Mode (Fallback):**
- 🔄 **Local Simulation**: If no API key
- 🔄 **Basic AI Agents**: Intelligent but limited
- 🔄 **Offline Operation**: No internet required

### 📁 **File Structure**

```
MVP/
├── .env                    # ✅ Your Duality AI API key (CONFIGURED)
├── config.env              # 📋 Template file
├── duality_ai_config.py    # 🔧 Configuration management
├── test_config.py          # 🧪 Configuration testing
├── main.py                 # 🚀 Main application
└── demo_final.py           # 🎮 Demo script
```

### 🔑 **API Key Management**

#### **Current API Key:**
- **Status**: ✅ Configured
- **Location**: `.env` file
- **Format**: JWT token
- **Expiry**: Valid until 2026

#### **To Update API Key:**
1. Edit `.env` file
2. Replace the `DUALITY_AI_API_KEY` value
3. Restart the application

#### **To Remove API Key:**
1. Delete or rename `.env` file
2. Application will switch to Local Mode

### 🧪 **Testing**

#### **Configuration Test:**
```bash
python test_config.py
```

#### **Demo Script:**
```bash
python demo_final.py
```

#### **Application Test:**
```bash
python main.py
```

### 🌐 **API Endpoints**

#### **With API Key (Current Mode):**
- `GET /` - Platform overview with API mode status
- `GET /health` - Health check with Duality AI API status
- `GET /api/v1/status` - API status with enhanced capabilities

#### **Expected API Response:**
```json
{
  "duality_ai": {
    "enabled": true,
    "mode": "API",
    "api_url": "https://api.duality.ai"
  }
}
```

### 🎯 **Hackathon Demo**

#### **Perfect Setup for Demo:**
1. ✅ **Duality AI API Key**: Configured
2. ✅ **API Mode**: Active
3. ✅ **Enhanced Features**: Available
4. ✅ **Sponsor Track**: Ready

#### **Demo Commands:**
```bash
# 1. Show configuration
python test_config.py

# 2. Run comprehensive demo
python demo_final.py

# 3. Start application
python main.py

# 4. Test API endpoints
curl http://localhost:8000/health
```

### 🔒 **Security Notes**

#### **API Key Security:**
- ✅ **Environment Variable**: Stored in `.env` file
- ✅ **Not in Code**: API key not hardcoded
- ✅ **Git Ignore**: `.env` should be in `.gitignore`
- ✅ **Template File**: `config.env` for reference

#### **Best Practices:**
- 🔒 Keep `.env` file secure
- 🔒 Don't commit API keys to version control
- 🔒 Use different keys for development/production
- 🔒 Rotate API keys regularly

### 🚀 **Ready for Presentation!**

Your GhostLAN SimWorld platform is:
- ✅ **Fully Configured** with Duality AI API
- ✅ **Running in API Mode** (enhanced capabilities)
- ✅ **Ready for Demo** with all features
- ✅ **Sponsor Track** compliant

**No additional setup required!** 🎯

---

*Powered by Duality AI* 🤖
*Advanced eSports Anti-Cheat Testing Platform* 