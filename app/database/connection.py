from motor.motor_asyncio import AsyncIOMotorClient

# Configurar la cadena de conexión a MongoDB (asegúrate de reemplazar con tus credenciales)
mongo_url = "mongodb+srv://cookiegpjr:L1Ihc9vGp5sRIMeK@clusterincubacion.is3n9.mongodb.net/?retryWrites=true&w=majority&appName=ClusterIncubacion"

client = AsyncIOMotorClient(mongo_url)
db = client['incubacion_db']  # Nombre de la base de datos
