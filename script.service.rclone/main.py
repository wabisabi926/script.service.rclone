import os
import stat
import subprocess
import xbmcaddon
import xbmcvfs
import logging
import time

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener la ruta del addon y la ubicación para copiar el archivo
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
src = os.path.join(addon_path, 'rclone-android-21-armv7a')
loc = xbmcvfs.translatePath("special://xbmcbin/../../../cache/lib/rclone-android-21-armv7a")

# Copiar y hacer el archivo ejecutable si no existe
if not xbmcvfs.exists(loc):
    if xbmcvfs.copy(src, loc):
        st = os.stat(loc)
        os.chmod(loc, st.st_mode | stat.S_IEXEC)
        logger.info(f"Copiado y hecho ejecutable: {loc}")
    else:
        logger.error(f"Error al copiar {src} a {loc}")
else:
    logger.info(f"El archivo ya existe: {loc}")

# Copiar el archivo rclone.conf proporcionado
rclone_conf_src = os.path.join(addon_path, 'rclone.conf')
rclone_conf_dest = xbmcvfs.translatePath("special://masterprofile/rclone.conf")
if not xbmcvfs.exists(rclone_conf_dest):
    if xbmcvfs.copy(rclone_conf_src, rclone_conf_dest):
        logger.info(f"rclone.conf copiado a: {rclone_conf_dest}")
    else:
        logger.error(f"Error al copiar {rclone_conf_src} a {rclone_conf_dest}")
else:
    logger.info(f"El archivo rclone.conf ya existe en: {rclone_conf_dest}")

# Obtener las ubicaciones del archivo de configuración, archivo pid y archivo de registro
pidfile = xbmcvfs.translatePath("special://temp/librclone.pid")
logfile = xbmcvfs.translatePath("special://temp/librclone.log")
cachepath = xbmcvfs.translatePath("special://temp")

# Obtener las opciones especificadas por el usuario
check_interval = int(addon.getSetting("check_interval"))
cache_time = int(addon.getSetting("cache_time"))
folder_to_watch = addon.getSetting("folder_to_watch")
remote_name = addon.getSetting("remote_name")
webdav_port = addon.getSetting("webdav_port")

# Ejecutar el archivo copiado con los argumentos especificados usando subprocess
cmd = [
    loc, 
    'serve', 'webdav', f'{remote_name}:{folder_to_watch}',
    '--addr', f':{webdav_port}',
    '--config', rclone_conf_dest,
    '--log-file', logfile,
    '--dir-cache-time', f'{cache_time}h',
    '--poll-interval', f'{check_interval}m',
    '--vfs-cache-mode', 'full',
    '--vfs-cache-max-size', '200M',  # Limitar el tamaño del caché a 200MB
    '--drive-chunk-size', '32M',
    '--transfers', '10'
]

try:
    subprocess.Popen(cmd)
    logger.info(f"Comando ejecutado: {' '.join(cmd)}")
except Exception as e:
    logger.error(f"Error al ejecutar el comando: {e}")

# Llamar a los scripts para actualizar la biblioteca de Kodi
try:
    subprocess.run(["python3", os.path.join(addon_path, "update_library.py")])
    subprocess.run(["python3", os.path.join(addon_path, "auto_update_kodi_library.py")])
except Exception as e:
    logger.error(f"Error al ejecutar scripts de actualización: {e}")
