from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import db  # Conexión a MongoDB

router = APIRouter()

class Observacion(BaseModel):
    huevo_id: str  # Referencia al ID del huevo
    porcentaje: float
    color: str
    rupturas: str
    contaminacion: str
    note: str

@router.post("/observacion/")
async def agregar_observacion(observacion: Observacion):
    try:
        result = await db.observaciones.insert_one(observacion.dict())
        return {"mensaje": "Observación agregada", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))