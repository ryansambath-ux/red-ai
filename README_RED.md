# Red AI 0.1

Red is a persistent personal AI operating layer: cloud brain + local device agents.

## First bootstrap
This branch establishes:
- FastAPI Red Core
- health/chat endpoints
- allow-listed tool registry
- proactive attention engine
- Docker/Google Cloud Run foundation
- secret-safe environment template

## Architecture
User -> voice/mobile/web -> Red Core -> reasoning/memory/tool router -> cloud tools + authenticated Windows agent.

## Run locally
1. Install Python 3.12.
2. Create a virtual environment.
3. Install: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload`
5. Open `http://127.0.0.1:8000/health`

## Security
Do not commit passwords, API keys or tokens. Computer-control tools will be allow-listed and authenticated. Consequential actions will require confirmation.

## Next
Connect the reasoning model, persistent memory, live information tools, Windows agent, voice and proactive monitors.
