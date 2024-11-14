from pydantic import BaseModel, Field
from typing import List

class IncubadoraModel(BaseModel):
    id: str = Field(None, alias="_id")
    Numero: int
    maples: List[str]

class MapleModel(BaseModel):
    id: str = Field(None, alias="_id")
    id_incubadora: str
    Serial: str
    posición: str
    huevos: List[List[str]]
    imagen: str

class HuevoModel(BaseModel):
    id: str = Field(None, alias="_id")
    id_maple: str
    posición: List[int]
    viabilidad: bool
    id_observaciones: List[str]

class ObservacionModel(BaseModel):
    id: str = Field(None, alias="_id")
    id_huevo: str
    porcentaje_inviabilidad: float
    fecha_analisis: str
    detalles_visuales: dict
    comentarios: str
