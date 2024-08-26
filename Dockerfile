# Usar una imagen base de Python ligera
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . .

# Exponer el puerto que usará la aplicación (en este caso 8080)
EXPOSE 8080

# Comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]