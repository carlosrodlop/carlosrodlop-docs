# Dockerfile para generar el mapa de ruta de Portugal 2025
FROM python:3.11-slim

# Metadatos del contenedor
LABEL maintainer="carlosrodlop"
LABEL description="Contenedor para generar mapas de ruta de viajes con Python y matplotlib"
LABEL version="1.0"

# Instalar dependencias del sistema necesarias para matplotlib
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements.txt primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del proyecto
COPY . .

# Crear directorio para los mapas generados
RUN mkdir -p /app/output

# Establecer variables de entorno para matplotlib (sin GUI)
ENV MPLBACKEND=Agg
ENV PYTHONUNBUFFERED=1

# Comando por defecto para ejecutar el script
CMD ["python", "portugal_route_map.py"]

# Exponer puerto si queremos servir los mapas via web (opcional)
EXPOSE 8000

# Información adicional
VOLUME ["/app/output"]
