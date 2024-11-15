from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Conexión a MongoDB Atlas
mongo_url = "mongodb+srv://cookiegpjr:L1Ihc9vGp5sRIMeK@clusterincubacion.is3n9.mongodb.net/?retryWrites=true&w=majority&appName=ClusterIncubacion"

client = MongoClient(mongo_url)
db = client["incubacion_db"]