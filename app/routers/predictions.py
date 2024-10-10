import cv2  # Para el procesamiento de imágenes
import numpy as np
from fastapi import APIRouter, HTTPException, File, UploadFile
from app.models.egg_model import EggData
from app.services.predictions import process_prediction, predecir_viabilidad
from app.models.neural_net import predecir_viabilidad
from app.database.connection import db
import shutil
import os
from datetime import datetime

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
    

# Verificar si la carpeta temp existe, y si no, crearla
if not os.path.exists("temp"):
    os.makedirs("temp")

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Verificar si el archivo tiene un formato permitido
        if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Formato de archivo no permitido. Solo se permiten archivos .jpg, .jpeg y .png.")

        # Guardar la imagen temporalmente
        ruta_imagen = f"temp/{file.filename}"
        with open(ruta_imagen, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Cargar la imagen para procesamiento en escala de grises
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        if imagen is None:
            raise HTTPException(status_code=400, detail="No se pudo procesar la imagen. Verifique el formato o si la imagen está corrupta.")

        # Realizar predicción usando el modelo cargado
        try:
            clasificacion, colorimetria, fisuras, viabilidad = predecir_viabilidad(imagen)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")

        # Insertar datos en la colección 'maple'
        maple_id = db.maple.insert_one({
            "incubadora_id": "ID_incu_bad",  # Reemplazar con los datos correctos
            "imagen": file.filename,
            "c_inviables": int(clasificacion)  # Usar lógica adecuada
        }).inserted_id

        # Insertar huevo en la colección 'huevos'
        huevo_id = db.huevos.insert_one({
            "maple_id": maple_id,
            "estado": 'viable' if viabilidad > 0.5 else 'inviable',
            "f_ingreso": datetime.now()  # Timestamp actual
        }).inserted_id

        # Insertar observaciones en la colección 'observaciones'
        db.observaciones.insert_one({
            "huevo_id": huevo_id,
            "color": str(colorimetria),
            "rupturas": 'fisura' if fisuras > 0.5 else 'sin fisura',
            "contaminacion": "no_detectada",  # Campo opcional
            "note": "Información adicional"
        })

        return {"mensaje": "Datos insertados correctamente", "maple_id": str(maple_id), "huevo_id": str(huevo_id)}

    except HTTPException as he:
        raise he  # Re-raise los errores HTTP como están
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

