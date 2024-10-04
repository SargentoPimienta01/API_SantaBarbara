from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predictions, healtcheck
from app.routers import maple
from app.routers import incubadora
from app.routers import huevo
from app.routers import observaciones

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

# Prueba inicial para verificar que el servidor está corriendo
@app.get("/")
def read_root():
    return {"message": "API Santa Barbara is running!"}
