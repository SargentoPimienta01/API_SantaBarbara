from fastapi import FastAPI
from app.routers import predictions, healthcheck

# Inicializar la aplicación FastAPI
app = FastAPI()

# Incluir las rutas definidas en los routers
app.include_router(predictions.router)
app.include_router(healthcheck.router)
