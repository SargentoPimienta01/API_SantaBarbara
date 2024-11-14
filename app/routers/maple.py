from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import db  # Conexión a MongoDB

router = APIRouter()

# Modelo de datos para la colección "maple"
class Maple(BaseModel):
    incubadora_id: str  # Aquí irá la referencia al ID de la incubadora
    imagen: str  # URL o ubicación de la imagen asociada
    c_inviables: int  # Cantidad de huevos inviables

# Ruta para agregar un nuevo "maple"
@router.post("/maple/")
async def agregar_maple(maple: Maple):
    try:
        # Insertar el documento en la colección "maple"
        result = await db.maple.insert_one(maple.dict())
        return {"mensaje": "Maple agregado", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
