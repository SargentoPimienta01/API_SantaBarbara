import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

# Definir las etiquetas de color
COLOR_LABELS = ["blanco", "marrón", "otro"]

# Crear el modelo de red neuronal convolucional para clasificación de color
def create_color_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(COLOR_LABELS), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Instanciar el modelo
color_model = create_color_model()

# Función para entrenar la red (esto se haría con un conjunto de datos de imágenes etiquetadas previamente)
def train_color_model(X_train, y_train, X_val, y_val, epochs=10, batch_size=32):
    y_train = tf.keras.utils.to_categorical(y_train, num_classes=len(COLOR_LABELS))
    y_val = tf.keras.utils.to_categorical(y_val, num_classes=len(COLOR_LABELS))
    color_model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)

# Función para predecir el color de un huevo basado en su imagen
def analyze_color(egg_image):
    # Preprocesamiento de la imagen para ser compatible con la entrada del modelo
    egg_image = cv2.resize(egg_image, (64, 64))  # Redimensiona la imagen a 64x64
    egg_image = img_to_array(egg_image) / 255.0  # Normaliza los valores de píxeles entre 0 y 1
    egg_image = np.expand_dims(egg_image, axis=0)  # Agrega una dimensión para el batch

    # Realizar la predicción de color
    prediction = color_model.predict(egg_image)
    color_index = np.argmax(prediction)
    color_name = COLOR_LABELS[color_index]

    return {"color": color_name, "confidence": prediction[0][color_index]}
