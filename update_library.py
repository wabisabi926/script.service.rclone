import os
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_source_path = "dav://127.0.0.1:23457/AriosTV"

check_interval = 600

def get_last_update_time():
    try:
        return os.path.getmtime(data_source_path)
    except Exception as e:
        logger.error(f"Error getting last modification time of {data_source_path}: {e}")

def update_kodi_library():
    try:
        subprocess.run(["xbmc-send", "-a", "UpdateLibrary(video)"])
        logger.info("Kodi library updated.")
    except Exception as e:
        logger.error(f"Error updating Kodi library: {e}")

last_update_time = get_last_update_time()

while True:
    current_update_time = get_last_update_time()

    if current_update_time != last_update_time:
        update_kodi_library()
        last_update_time = current_update_time

    time.sleep(check_interval)