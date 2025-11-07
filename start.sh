#!/bin/bash

# Inicia el servidor Ollama en background
ollama serve &

# Espera a que el servicio Ollama abra el puerto (ajusta si hace falta)
sleep 8

# Si el modelo CDT no existe, créalo usando el Modelfile incluido
# (grep busca la cadena "CDT" en la lista; si no existe, lo crea)
if ! ollama list | grep -q "CDT"; then
  echo "CDT no encontrado. Creando modelo desde Modelfile..."
  ollama create CDT -f Modelfile
  echo "Creación de CDT finalizada."
else
  echo "Modelo CDT ya existe."
fi

# Inicia la API (Uvicorn)
uvicorn server:app --host 0.0.0.0 --port 10000
