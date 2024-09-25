import tensorflow as tf

# Ruta al archivo del modelo de la red neuronal
MODEL_PATH = 'ruta_a_tu_modelo.h5'

# Cargar el modelo de la red neuronal
model = tf.keras.models.load_model(MODEL_PATH)

# Función para predecir la viabilidad de los huevos
def predict_viability(data):
    # Asegurarse de que los datos están en el formato correcto
    prediction = model.predict(data)
    return prediction
