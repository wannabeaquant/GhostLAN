# GhostLAN SimWorld

## What This Is
Digital twin simulation platform for offline eSports anti-cheat testing, powered by Duality AI.
10 AI agents (6 normal, 4 configurable cheaters). Match recording, tournament management, real-time streaming.
Hackathon project.

## Stack
- Python 3.8+ / FastAPI
- SQLite (ghostlan.db)
- Duality AI API (already configured in .env)
- JWT authentication
- WebSocket (real-time events)
- Docker (production deployment)

## Commands
```bash
pip install -r requirements.txt
python main.py              # Start platform
python test_config.py       # Test Duality AI config
python demo_final.py        # Full demo run
python test_system.py       # All tests
python -m pytest tests/

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
docker build -t ghostlan-simworld . && docker run -p 8000:8000 ghostlan-simworld
```
- Web: http://localhost:8000 | Docs: http://localhost:8000/docs

## Architecture
```
MVP/
  duality_scene/       # Duality AI simulation environment
  ghostlan_core/       # Anti-cheat detection engine
  analytics/           # Performance analytics + reporting
  api/                 # REST endpoints
  streaming/           # Real-time streaming
  mobile/              # Mobile app backend
  cloud_integration/   # Cloud deployment
  advanced_tournament/ # Tournament features
  Frontend/            # Web dashboards
  main.py              # Entry point
```

## GitHub
https://github.com/wannabeaquant/GhostLAN
