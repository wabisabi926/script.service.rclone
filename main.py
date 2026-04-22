import os
import stat
import subprocess
import xbmcaddon
import xbmcvfs
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
src = os.path.join(addon_path, 'bin', 'rclone-coreelec-arm64')
loc = xbmcvfs.translatePath("special://xbmcbin/../../../cache/lib/rclone-coreelec-arm64")

if not xbmcvfs.exists(loc):
    if xbmcvfs.exists(src):
        if xbmcvfs.copy(src, loc):
            try:
                st = os.stat(loc)
                os.chmod(loc, st.st_mode | stat.S_IEXEC)
                logger.info(f"Copied and made executable: {loc}")
            except Exception as e:
                logger.error(f"Error setting permissions: {e}")
        else:
            logger.error(f"Error copying {src} to {loc}")
    else:
        logger.error(f"Source file not found: {src}")
else:
    logger.info(f"File already exists: {loc}")

rclone_conf_src = os.path.join(addon_path, 'rclone.conf')
rclone_conf_dest = xbmcvfs.translatePath("special://masterprofile/rclone.conf")
if not xbmcvfs.exists(rclone_conf_dest):
    if xbmcvfs.exists(rclone_conf_src):
        if xbmcvfs.copy(rclone_conf_src, rclone_conf_dest):
            logger.info(f"rclone.conf copied to: {rclone_conf_dest}")
        else:
            logger.error(f"Error copying {rclone_conf_src} to {rclone_conf_dest}")
    else:
        logger.error(f"Source config file not found: {rclone_conf_src}")
else:
    logger.info(f"rclone.conf already exists at: {rclone_conf_dest}")

pidfile = xbmcvfs.translatePath("special://temp/librclone.pid")
logfile = xbmcvfs.translatePath("special://temp/librclone.log")
cachepath = xbmcvfs.translatePath("special://temp")

try:
    check_interval = int(addon.getSetting("check_interval"))
    cache_time = int(addon.getSetting("cache_time"))
    folder_to_watch = addon.getSetting("folder_to_watch")
    remote_name = addon.getSetting("remote_name")
    webdav_port = addon.getSetting("webdav_port")
except Exception as e:
    logger.error(f"Error getting settings: {e}")
    check_interval = 5
    cache_time = 10
    folder_to_watch = ""
    remote_name = "remote"
    webdav_port = "8080"

if xbmcvfs.exists(loc):
    cmd = [
        loc,
        'serve', 'webdav', f'{remote_name}:{folder_to_watch}',
        '--addr', f':{webdav_port}',
        '--config', rclone_conf_dest,
        '--log-file', logfile,
        '--dir-cache-time', f'{cache_time}h',
        '--poll-interval', f'{check_interval}m',
        '--vfs-cache-mode', 'full',
        '--vfs-cache-max-size', '200M',
        '--drive-chunk-size', '32M',
        '--transfers', '10'
    ]

    try:
        subprocess.Popen(cmd)
        logger.info(f"Command executed: {' '.join(cmd)}")
    except Exception as e:
        logger.error(f"Error executing command: {e}")
else:
    logger.error(f"Executable not found: {loc}")

try:
    update_library_script = os.path.join(addon_path, "update_library.py")
    auto_update_script = os.path.join(addon_path, "auto_update_kodi_library.py")

    if xbmcvfs.exists(update_library_script):
        subprocess.run(["python3", update_library_script])
    else:
        logger.warning(f"Update script not found: {update_library_script}")

    if xbmcvfs.exists(auto_update_script):
        subprocess.run(["python3", auto_update_script])
    else:
        logger.warning(f"Auto update script not found: {auto_update_script}")
except Exception as e:
    logger.error(f"Error executing update scripts: {e}")