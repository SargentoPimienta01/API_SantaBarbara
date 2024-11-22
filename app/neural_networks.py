import cv2
import numpy as np
import tensorflow as tf
from keras import models
import uuid

# Cargar el modelo entrenado
model = models.load_model("app/neural_networks.py")

def generate_unique_id():
    """Genera un ID único para cada huevo detectado."""
    return str(uuid.uuid4())

def detect_eggs(image_content):
    """Detecta huevos y devuelve sus posiciones y características."""
    # Convierte el contenido de la imagen en un arreglo
    nparr = np.frombuffer(image_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Preprocesa la imagen para el modelo
    input_image = cv2.resize(image, (224, 224))  # Ajustar al tamaño que requiere el modelo
    input_image = input_image / 255.0  # Normalizar entre 0 y 1
    input_image = np.expand_dims(input_image, axis=0)  # Agregar una dimensión para el batch

    # Realiza la predicción
    predictions = model.predict(input_image)

    # Procesa la salida del modelo
    eggs_data = []
    for i, prediction in enumerate(predictions):
        egg_id = generate_unique_id()
        # Ejemplo de extracción de características (ajusta según tu modelo):
        viabilidad = "viable" if prediction[0] > 0.5 else "inviable"
        position = [i // 15, i % 15]  # Suponiendo un arreglo de 10x15 huevos
        eggs_data.append({
            "id_huevo": egg_id,
            "viabilidad": viabilidad,
            "position": position
        })

    return eggs_data
