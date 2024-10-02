from fastapi import APIRouter, HTTPException
from app.database.connection import db
from pydantic import BaseModel

router = APIRouter()

# Definir el modelo de datos para una incubadora
class Incubadora(BaseModel):
    name: str
    capacidad: int
    u_mantenimiento: str

# Ruta para agregar una incubadora
@router.post("/incubadora/")
async def agregar_incubadora(incubadora: Incubadora):
    try:
        result = await db.incubadora.insert_one(incubadora.dict())
        return {"mensaje": "Incubadora agregada", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

