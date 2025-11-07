from fastapi import FastAPI, Request
import subprocess, requests, os, threading, time

app = FastAPI()

# 1️⃣ Inicia el servidor Ollama en segundo plano
def start_ollama():
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

threading.Thread(target=start_ollama, daemon=True).start()

# Espera unos segundos a que inicie
time.sleep(5)

# 2️⃣ Endpoint raíz
@app.get("/")
def root():
    return {"status": "Ollama server is running"}

# 3️⃣ Endpoint de generación
@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    response = requests.post("http://localhost:11434/api/generate", json=data)
    return response.json()
