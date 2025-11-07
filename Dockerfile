# Usa una imagen base compatible con Ollama
FROM ubuntu:22.04

# Instala dependencias básicas
RUN apt-get update && apt-get install -y curl python3 python3-pip

# Instala Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copia los archivos de tu app
WORKDIR /app
COPY . .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 10000

# Inicia Ollama + tu API
CMD ["sh", "-lc", "ollama serve & sleep 5 && ollama create CDT -f Modelfile && uvicorn server:app --host 0.0.0.0 --port ${PORT:-10000}"]
# Reemplaza "CDT" y "Modelfile" con el nombre y archivo de tu modelo Ollama

