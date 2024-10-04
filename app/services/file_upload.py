import shutil
import os

# Verificar si la carpeta temp existe, y si no, crearla
if not os.path.exists("temp"):
    os.makedirs("temp")

def guardar_imagen_temporalmente(file):
    ruta_imagen = f"temp/{file.filename}"
    with open(ruta_imagen, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return ruta_imagen
