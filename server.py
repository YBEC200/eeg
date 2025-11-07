from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import subprocess, threading, time, os

app = FastAPI()

# Habilitar CORS para permitir llamadas desde el navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # en producción pon tu dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (opcional) Inicia Ollama en background si no lo hace start.sh (definitivamente se inicia en start.sh)
def start_ollama_if_missing():
    # Si no existe el binario, no hace nada
    if not os.path.exists("/usr/local/bin/ollama") and not os.path.exists("/usr/bin/ollama"):
        return
    # Comprueba si el puerto responde; si no, levanta ollama local
    try:
        requests.get("http://127.0.0.1:11434", timeout=1)
        return
    except:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Llamamos (esto no hará daño si start.sh ya inició ollama)
threading.Thread(target=start_ollama_if_missing, daemon=True).start()
time.sleep(2)

@app.get("/")
def root():
    return {"status": "Ollama server is running"}

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    model = data.get("model", "CDT")
    prompt = data.get("prompt", "")

    try:
        # Llamada al servidor Ollama local dentro del contenedor
        r = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120
        )
        # r.json() debe contener la clave "response" según cómo Ollama devuelva el resultado
        j = r.json()
        text = j.get("response") or j.get("output") or str(j)
        return {"response": text}
    except Exception as e:
        return {"response": f"Error llamando al modelo: {str(e)}"}
