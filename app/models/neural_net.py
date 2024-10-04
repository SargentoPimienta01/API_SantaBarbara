import cv2  # Para el procesamiento de imágenes
import numpy as np  # Para operaciones numéricas con matrices
import tensorflow as tf
from keras import layers, models

# Cargar el modelo de la red neuronal entrenada una sola vez
model = tf.keras.models.load_model('/Users/Alex/Desktop/ISI/Python/ProyectoSantaBarbara/modelo_cnn.h5')

# Definir el modelo CNN mejorado con salidas múltiples
def crear_modelo_cnn_mejorado(tamaño_imagen=(128, 128)):
    entrada = layers.Input(shape=(tamaño_imagen[0], tamaño_imagen[1], 1))

    # Bloque convolucional 1
    x = layers.Conv2D(32, (3, 3), activation='relu')(entrada)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.BatchNormalization()(x)
    
    # Bloque convolucional 2
    x = layers.Conv2D(64, (3, 3), activation='relu')(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.BatchNormalization()(x)

    # Bloque convolucional 3
    x = layers.Conv2D(128, (3, 3), activation='relu')(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.BatchNormalization()(x)

    # Aplanar y añadir capas densas
    x = layers.Flatten()(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.5)(x)

    # Salida 1: Clasificación (huevo/no huevo)
    salida_clasificacion = layers.Dense(1, activation='sigmoid', name='clasificacion')(x)

    # Salida 2: Colorimetría (ej. RGB normalizado)
    salida_colorimetria = layers.Dense(3, activation='softmax', name='colorimetria')(x)

    # Salida 3: Detección de fisuras (fisura/no fisura)
    salida_fisuras = layers.Dense(1, activation='sigmoid', name='fisuras')(x)

    # Salida 4: Porcentaje de viabilidad
    salida_viabilidad = layers.Dense(1, activation='sigmoid', name='viabilidad')(x)

    # Definir el modelo con múltiples salidas
    modelo = models.Model(inputs=entrada, outputs=[salida_clasificacion, salida_colorimetria, salida_fisuras, salida_viabilidad])
    
    modelo.compile(optimizer='adam', 
                   loss={'clasificacion': 'binary_crossentropy', 
                         'colorimetria': 'categorical_crossentropy',
                         'fisuras': 'binary_crossentropy',
                         'viabilidad': 'binary_crossentropy'},
                   metrics={'clasificacion': 'accuracy',
                            'colorimetria': 'accuracy',
                            'fisuras': 'accuracy',
                            'viabilidad': 'accuracy'})
    
    return modelo

# Función para detectar huevos
def detectar_huevos(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para eliminar ruido
    imagen_gris = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

    # Aplicar binarización adaptativa para mejorar la detección
    _, imagen_bin = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Detectar bordes usando Canny Edge Detection
    bordes = cv2.Canny(imagen_bin, 50, 150)

    # Encontrar contornos en la imagen
    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    huevos_detectados = []
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

# Función para predecir la viabilidad y características
def predecir_viabilidad(imagen):
    huevos, error = detectar_huevos(imagen)
    
    if error:
        return {"mensaje": error, "detalles": None}
    
    resultados = []
    for huevo in huevos:
        huevo = np.expand_dims(huevo, axis=0)  # Expandir dimensiones para el batch

        # Obtener las predicciones de la red neuronal
        clasificacion, colorimetria, fisuras, viabilidad = model.predict(huevo)

        # Convertir resultados a valores comprensibles
        resultado = {
            "clasificacion": "huevo" if clasificacion > 0.5 else "no_huevo",
            "colorimetria": colorimetria.tolist(),  # Normalizado en RGB
            "fisuras": "fisura" if fisuras > 0.5 else "sin_fisura",
            "viabilidad": f"{viabilidad[0] * 100:.2f}%"  # Convertir a porcentaje
        }
        resultados.append(resultado)
    
    return {"mensaje": "Procesamiento completo", "detalles": resultados}
