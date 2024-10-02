from fastapi import APIRouter, HTTPException
from app.models.egg_model import EggData
from app.services.predictions import process_prediction

router = APIRouter()

# Ruta para procesar las predicciones de viabilidad y guardar los huevos detectados
@router.post("/predict/{incubadora_id}/{maple_id}/")
async def predict_egg_viability(egg_data: EggData, incubadora_id: str, maple_id: str):
    try:
        # Procesar la predicción y manejar la detección de huevos
        result = await process_prediction(egg_data, incubadora_id, maple_id)
        if "message" in result:
            # Si no se encontraron huevos, devolver el mensaje sin probabilidad
            return {"message": result["message"]}
        
        # Devolver la información sobre los huevos detectados y su viabilidad
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
