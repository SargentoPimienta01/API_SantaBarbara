from app.models.neural_net import predict_viability
from app.database.connection import db

# Función para procesar la predicción y guardar el resultado en MongoDB
async def process_prediction(egg_data):
    # Convertir los datos en el formato correcto para la red neuronal
    data = egg_data.data
    prediction = predict_viability(data)

    # Guardar la predicción en MongoDB
    result = await db.predictions.insert_one({
        "data": egg_data.data,
        "prediction": prediction.tolist()
    })

    return prediction
