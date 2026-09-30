@echo off
cd /d "%~dp0\.."
python -m windows_agent.server
pause
