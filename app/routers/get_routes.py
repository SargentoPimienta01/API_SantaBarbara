from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List
from pydantic import BaseModel
from app.database import db 

router = APIRouter()

# Modelo de datos para obtener datos de 'huevos' (modificar según tus campos)
class Huevo(BaseModel):
    id: str
    maple_id: str
    estado: str
    f_ingreso: str

# 1. Ruta GET para obtener todos los huevos
@router.get("/huevos/", response_model=List[Huevo])
async def obtener_huevos():
    try:
        huevos = await db.huevos.find().to_list(100)  # Limitar a 100 documentos
        return huevos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Ruta GET para obtener un huevo por su ID
@router.get("/huevos/{huevo_id}", response_model=Huevo)
async def obtener_huevo(huevo_id: str):
    try:
        huevo = await db.huevos.find_one({"_id": ObjectId(huevo_id)})
        if huevo is None:
            raise HTTPException(status_code=404, detail="Huevo no encontrado")
        return huevo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Ruta GET para obtener todos los datos de la incubadora
@router.get("/incubadora/{incubadora_id}")
async def obtener_incubadora(incubadora_id: str):
    try:
        incubadora = await db.incubadora.find_one({"_id": ObjectId(incubadora_id)})
        if incubadora is None:
            raise HTTPException(status_code=404, detail="Incubadora no encontrada")
        return incubadora
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Ruta GET para obtener todas las observaciones
@router.get("/observaciones/")
async def obtener_observaciones():
    try:
        observaciones = await db.observaciones.find().to_list(100)  # Limitar a 100 documentos
        return observaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
