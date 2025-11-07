#!/bin/bash
ollama serve &
sleep 5
uvicorn server:app --host 0.0.0.0 --port 10000
