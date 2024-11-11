import numpy as np
import pandas as pd
from .feedback_model import entrenar_modelo_feedback, predecir_feedback
import tensorflow as tf

# Datos de ejemplo para las salidas de las redes y datos adicionales
# Estos deberían ser reemplazados con datos reales en producción

# Ejemplo de las salidas de las dos redes neuronales existentes
salida_red_1 = np.array([0.85, 0.4, 0.9])  # Probabilidad de viabilidad (ejemplo)
salida_red_2 = np.array([0.8, 0.3, 0.88])  # Otra métrica de viabilidad o detalles adicionales (ejemplo)

# Datos adicionales de maple, incubadora y especificaciones del huevo
maple_data = np.array([1, 2, 1])  # Identificador o clasificación del maple
incubadora_data = np.array([101, 102, 101])  # Número de incubadora (ejemplo)
detalle_huevo_data = np.array([5, 3, 4])  # Datos específicos del huevo (ej. tamaño o peso)

# Consolidar todas las entradas en un DataFrame
datos_entrada = pd.DataFrame({
    'salida_red_1': salida_red_1,
    'salida_red_2': salida_red_2,
    'maple': maple_data,
    'incubadora': incubadora_data,
    'detalle_huevo': detalle_huevo_data
})

# Definir etiquetas de ejemplo para la retroalimentación (esto es sólo un ejemplo)
# En un escenario real, estos datos serían obtenidos de la clasificación esperada
etiquetas = np.array([1, 0, 1])  # Ejemplo de etiquetas binarias (viable o no viable)

# Entrenar el modelo de retroalimentación con los datos preparados
modelo_feedback = entrenar_modelo_feedback(datos_entrada, etiquetas)

# Realizar predicciones e interpretaciones
prediccion = predecir_feedback(modelo_feedback, datos_entrada)
print("Interpretación de retroalimentación:", prediccion)
