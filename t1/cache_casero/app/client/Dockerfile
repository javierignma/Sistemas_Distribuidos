# Usa una imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el código fuente al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Expone el puerto en el que se ejecuta la aplicación (ajusta esto según tu necesidad)
EXPOSE 50051
EXPOSE 5000

ENTRYPOINT ["python", "server.py"]

