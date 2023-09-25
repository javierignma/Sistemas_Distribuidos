# Usa una imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el código fuente al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Expone el puerto en el que se ejecuta la aplicación (ajusta esto según tu necesidad)
EXPOSE 5000
EXPOSE 11211

CMD ["sh", "-c", "while true; do sleep 1000; done"]
#ENTRYPOINT ["python", "server.py"]