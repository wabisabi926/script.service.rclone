import os
import time
import subprocess
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define la ruta de la fuente de datos
data_source_path = "dav://127.0.0.1:23457/AriosTV"

# Define el intervalo de tiempo en segundos en el que se comprobará si hay nuevo contenido
check_interval = 600 # 10 minutos

# Obtiene el tiempo de la última modificación de la fuente de datos
def get_last_update_time():
    try:
        return os.path.getmtime(data_source_path)
    except Exception as e:
        logger.error(f"Error al obtener el tiempo de última modificación de {data_source_path}: {e}")

def update_kodi_library():
    try:
        subprocess.run(["xbmc-send", "-a", "UpdateLibrary(video)"])
        logger.info("Biblioteca de Kodi actualizada.")
    except Exception as e:
        logger.error(f"Error al actualizar la biblioteca de Kodi: {e}")

last_update_time = get_last_update_time()

while True:
    # Obtiene el tiempo de la última modificación de la fuente de datos
    current_update_time = get_last_update_time()

    # Si el tiempo de la última modificación es diferente al tiempo guardado
    if current_update_time != last_update_time:
        # Actualiza la biblioteca de Kodi
        update_kodi_library()
        # Guarda el nuevo tiempo de última modificación
        last_update_time = current_update_time

    # Duerme el script por el intervalo de tiempo definido
    time.sleep(check_interval)
