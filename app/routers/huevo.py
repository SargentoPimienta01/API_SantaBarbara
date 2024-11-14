from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import db  # Conexión a MongoDB

router = APIRouter()

class Huevo(BaseModel):
    maple_id: str  # Referencia al ID del maple
    estado: str
    posicion: str
    f_ingreso: str  # Fecha de ingreso del huevo

@router.post("/huevo/")
async def agregar_huevo(huevo: Huevo):
    try:
        result = await db.huevos.insert_one(huevo.dict())
        return {"mensaje": "Huevo agregado", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))