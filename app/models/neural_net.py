import tensorflow as tf
import cv2  # Para el procesamiento de imágenes
import numpy as np  # Para operaciones numéricas con matrices

# Cargar el modelo de la red neuronal entrenada
model = tf.keras.models.load_model('ruta_al_modelo/modelo_cnn.h5')

def predecir_viabilidad(imagen):
    # Redimensionar y normalizar la imagen antes de hacer la predicción
    imagen = cv2.resize(imagen, (128, 128))
    imagen = imagen / 255.0
    imagen = np.expand_dims(imagen, axis=0)  # Añadir la dimensión necesaria

    # Hacer la predicción de viabilidad usando el modelo
    prediccion = model.predict(imagen)
    return prediccion[0][0]  # Devolver la probabilidad de viabilidad

def detectar_huevos(imagen):
    huevos_detectados = []
    
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para eliminar ruido
    imagen_gris = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

    # Detectar bordes usando Canny Edge Detection
    bordes = cv2.Canny(imagen_gris, 50, 150)

    # Encontrar contornos en la imagen
    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        # Crear un rectángulo alrededor de cada contorno (huevo)
        x, y, w, h = cv2.boundingRect(contorno)
        huevo = imagen[y:y + h, x:x + w]

        # Redimensionar el huevo a un tamaño fijo
        huevo = cv2.resize(huevo, (128, 128))

        # Normalizar la imagen
        huevo = huevo / 255.0

        # Guardar el huevo detectado
        huevos_detectados.append(huevo)

    if len(huevos_detectados) == 0:
        return [], "No se detectaron huevos en la imagen."

    return np.array(huevos_detectados), None  # Devolver los huevos y sin errores
