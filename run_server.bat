@echo off
REM Sync dependencies using uv
uv sync
REM Launch uvicorn with config
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level info
