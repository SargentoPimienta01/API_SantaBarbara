from app.models.neural_net import predecir_viabilidad, detectar_huevos
from app.database import db
import cv2
import numpy as np
from datetime import datetime
from fastapi import HTTPException

# Función para procesar la predicción y guardar el resultado en MongoDB
async def process_prediction(egg_data, incubadora_id, maple_id):
    try:
        # Convertir los datos de entrada en el formato correcto (ajustar según sea necesario)
        imagen = np.array(egg_data.data).reshape(128, 128, 3)  # Asegúrate de que las dimensiones sean correctas

        # Preprocesar la imagen y detectar huevos
        huevos, error = detectar_huevos(imagen)

        if error:
            # Si no se encontraron huevos, devolvemos el mensaje de error
            return {"message": error}

        # Si se detectaron huevos, proceder a la predicción
        huevos_insertados = []
        for i, huevo in enumerate(huevos):
            try:
                # Usar la red neuronal para predecir la viabilidad del huevo
                probabilidad_viabilidad = predecir_viabilidad(huevo)

                # Definir el estado del huevo basado en la predicción
                estado = "viable" if probabilidad_viabilidad >= 0.5 else "inviable"

                # Datos del huevo para insertar en la base de datos
                huevo_data = {
                    "maple_id": maple_id,
                    "estado": estado,
                    "posicion": f"posicion_{i+1}",
                    "f_ingreso": datetime.utcnow()
                }

                # Insertar el huevo en la colección "huevos"
                huevo_result = await db.huevos.insert_one(huevo_data)
                huevo_id = huevo_result.inserted_id

                # Datos adicionales (observaciones) sobre el huevo
                observaciones_data = {
                    "huevo_id": huevo_id,
                    "color": "blanco",  # Ajusta esto según el análisis de colorimetría
                    "rupturas": "ninguna",  # Ajusta según el análisis de fisuras
                    "contaminacion": "ninguna",  # Ajusta según cualquier otra detección
                    "note": f"Huevo detectado con viabilidad {probabilidad_viabilidad:.2f}"
                }

                # Insertar las observaciones en la colección "observaciones"
                await db.observaciones.insert_one(observaciones_data)

                # Agregar el huevo insertado a la lista
                huevos_insertados.append(huevo_data)

            except Exception as e:
                # Si algo falla al procesar un huevo, registrar el error y continuar
                print(f"Error procesando el huevo {i+1}: {str(e)}")
                continue

        # Actualizar la colección "maple" con la cantidad de huevos inviables detectados
        await db.maple.update_one(
            {"_id": maple_id},
            {"$set": {"c_inviables": len([h for h in huevos_insertados if h['estado'] == 'inviable'])}}
        )

        return {"huevos_detectados": len(huevos_insertados), "huevos": huevos_insertados}

    except Exception as e:
        # Manejo de excepciones generales
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
