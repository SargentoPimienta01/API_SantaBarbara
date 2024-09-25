from pydantic import BaseModel

# Modelo de datos que recibiremos en las solicitudes POST
class EggData(BaseModel):
    data: list  # Datos que representan las características de un huevo
