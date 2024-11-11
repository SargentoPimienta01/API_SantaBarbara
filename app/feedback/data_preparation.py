import numpy as np
import pandas as pd

# Ejemplo de las salidas de las redes previas y datos adicionales
# Estas serían las salidas de las redes ya entrenadas y los datos adicionales para cada huevo

# Datos de ejemplo de salida de la primera red (clasificación de viabilidad)
salida_red_1 = np.array([0.85, 0.4, 0.9])  # Probabilidad de viabilidad (ejemplo)

# Datos de ejemplo de salida de la segunda red en la API (puede incluir otros aspectos)
salida_red_2 = np.array([0.8, 0.3, 0.88])  # Otra métrica de viabilidad o detalles adicionales (ejemplo)

# Datos adicionales de maple, incubadora y especificaciones del huevo
maple_data = np.array([1, 2, 1])  # Identificador o clasificación del maple
incubadora_data = np.array([101, 102, 101])  # Número de incubadora (ejemplo)
detalle_huevo_data = np.array([5, 3, 4])  # Datos específicos del huevo (ej. tamaño o peso)

# Combinar las salidas y datos adicionales en una sola estructura de datos
datos_entrada = pd.DataFrame({
    'salida_red_1': salida_red_1,
    'salida_red_2': salida_red_2,
    'maple': maple_data,
    'incubadora': incubadora_data,
    'detalle_huevo': detalle_huevo_data
})

# Visualizar la estructura de datos de entrada para verificar
print(datos_entrada)
