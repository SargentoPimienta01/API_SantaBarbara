from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from app.routers import predictions, healtcheck, maple, incubadora, huevo, observaciones, get_routes
from feedback.data_preparation import entrenar_modelo_feedback, predecir_feedback

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configurar CORS para permitir solicitudes desde cualquier origen
# Si deseas limitar a un dominio específico, cambia "*" por el dominio, por ejemplo: "http://localhost:3000"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir las rutas definidas en los routers
app.include_router(predictions.router)
app.include_router(healtcheck.router)
app.include_router(maple.router)
app.include_router(incubadora.router)
app.include_router(huevo.router)
app.include_router(observaciones.router)
app.include_router(get_routes.router)

# Prueba inicial para verificar que el servidor está corriendo
@app.get("/")
def read_root():
    return {"message": "API Santa Barbara is running!"}

# Modelo para recibir datos del frontend en el endpoint de retroalimentación
class FeedbackRequest(BaseModel):
    salida_red_1: list[float]
    salida_red_2: list[float]
    maple: list[int]
    incubadora: list[int]
    detalle_huevo: list[int]
    etiquetas: list[int]  # Etiquetas para el entrenamiento (opcional)

# Inicialización del modelo de retroalimentación en el arranque de la API
modelo_feedback = None

@app.on_event("startup")
def startup_event():
    global modelo_feedback
    # Configura etiquetas iniciales (datos de ejemplo) para el entrenamiento del modelo
    etiquetas = [1, 0, 1]  # Reemplaza con etiquetas reales si es necesario
    # Entrenar el modelo de retroalimentación con datos de ejemplo
    datos_entrada = pd.DataFrame({
        'salida_red_1': [0.85, 0.4, 0.9],
        'salida_red_2': [0.8, 0.3, 0.88],
        'maple': [1, 2, 1],
        'incubadora': [101, 102, 101],
        'detalle_huevo': [5, 3, 4]
    })
    modelo_feedback = entrenar_modelo_feedback(datos_entrada, etiquetas)

# Endpoint para la retroalimentación
@app.post("/feedback")
def feedback(request: FeedbackRequest):
    try:
        # Preparar el DataFrame con los datos recibidos
        datos = {
            'salida_red_1': request.salida_red_1,
            'salida_red_2': request.salida_red_2,
            'maple': request.maple,
            'incubadora': request.incubadora,
            'detalle_huevo': request.detalle_huevo
        }
        datos_entrada = pd.DataFrame(datos)

        # Realizar predicciones con el modelo de retroalimentación
        prediccion = predecir_feedback(modelo_feedback, datos_entrada)

        # Retornar la interpretación
        return {"interpretacion": prediccion.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la retroalimentación: {e}")
