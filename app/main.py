from fastapi import FastAPI, HTTPException, UploadFile, File
from database import db
from models import IncubadoraModel, MapleModel, HuevoModel, ObservacionModel
from analysis import analyze_maple_image

app = FastAPI()

@app.post("/maple/procesar")
async def procesar_maple(id_incubadora: str, file: UploadFile = File(...)):
    content = await file.read()
    results = analyze_maple_image(content)
    maple_data = {
        "id_incubadora": id_incubadora,
        "imagen": content,
        "huevos": results["huevos"],
        "Serial": results["serial"]
    }
    db["maple"].insert_one(maple_data)
    return results

@app.get("/incubadoras/{id}")
async def get_incubadora(id: str):
    result = db["incubadora"].find_one({"_id": id})
    if not result:
        raise HTTPException(status_code=404, detail="Incubadora no encontrada")
    return result

@app.get("/huevos/{id}")
async def get_huevo(id: str):
    result = db["huevo"].find_one({"_id": id})
    if not result:
        raise HTTPException(status_code=404, detail="Huevo no encontrado")
    return result

@app.post("/huevos/{id_huevo}/observacion")
async def agregar_observacion(id_huevo: str, observacion: ObservacionModel):
    observacion.id_huevo = id_huevo
    db["observaciones"].insert_one(observacion.dict(by_alias=True))
    return {"mensaje": "Observación agregada"}
