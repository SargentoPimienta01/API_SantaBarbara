from fastapi import APIRouter, HTTPException
from app.models.egg_model import EggData
from app.services.predictions import process_prediction

router = APIRouter()

# Ruta para procesar las predicciones de viabilidad
@router.post("/predict/")
async def predict_egg_viability(egg_data: EggData):
    try:
        # Procesar la predicción y devolver el resultado
        prediction = await process_prediction(egg_data)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
