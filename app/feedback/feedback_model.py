import tensorflow as tf

layers = tf.keras.layers
models = tf.keras.models
import pandas as pd

# Función para crear el modelo de retroalimentación
def crear_modelo_feedback(input_shape):
    modelo = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Dense(64, activation='relu'),  # Capa densa para aprendizaje profundo
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # Salida binaria o unitaria para interpretación
    ])
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return modelo

# Función para entrenar el modelo con los datos de entrada
def entrenar_modelo_feedback(datos_entrada, etiquetas):
    input_shape = (datos_entrada.shape[1],)  # Dimensión de entrada basada en el DataFrame
    modelo = crear_modelo_feedback(input_shape)
    
    # Entrenamiento del modelo
    modelo.fit(datos_entrada, etiquetas, epochs=10, batch_size=4)  # Ajusta los epochs y batch según necesidades
    
    return modelo

# Función para hacer predicciones e interpretaciones
def predecir_feedback(modelo, datos_nuevos):
    return modelo.predict(datos_nuevos)
