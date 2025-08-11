# Imagen base ligera y optimizada
FROM python:3.11-slim

# Previene prompts interactivos al instalar paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia tus archivos al contenedor
COPY requirements.txt .
COPY main.py .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Inicia la app
CMD ["python", "main.py"]
