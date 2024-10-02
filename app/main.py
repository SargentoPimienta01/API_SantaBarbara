from fastapi import FastAPI
from app.routers import predictions, healthcheck
from app.routers import maple
from app.routers import incubadora
from app.routers import huevo
from app.routers import observaciones

# Inicializar la aplicación FastAPI
app = FastAPI()

# Incluir las rutas definidas en los routers
app.include_router(predictions.router)
app.include_router(healthcheck.router)


#Crear Colecciones
app.include_router(maple.router)
app.include_router(incubadora.router)
app.include_router(huevo.router)
app.include_router(observaciones.router)
