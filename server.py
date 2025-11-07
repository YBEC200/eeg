from fastapi import FastAPI, Request
import subprocess, requests, os, threading, time
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# 🔧 Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes poner tu dominio HTML aquí en lugar de *
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
    model = data.get("model", "CDT")
    prompt = data.get("prompt", "")
    
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": model, "prompt": prompt},
        stream=False
    )
    
    return {"response": response.json().get("response", "")}
