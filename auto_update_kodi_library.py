import xbmc
import xbmcgui
import xbmcaddon
import time
import subprocess

ADDON = xbmcaddon.Addon()
RCLONE_CMD = ADDON.getSetting('rclone_cmd') + ' --disable-http2'

def update_library():
    subprocess.call([RCLONE_CMD, 'sync', 'remote:media', '/path/to/media'])
    xbmc.executebuiltin('UpdateLibrary(video)')

if __name__ == '__main__':
    while not xbmc.abortRequested:
        update_library()
        time.sleep(3600)  # Check every hour
