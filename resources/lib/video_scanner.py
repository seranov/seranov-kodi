import os
import threading
import time
import random
import xbmcvfs
import xbmc

from resources.lib.play_list import PlayListExtended
from resources.lib.plugin_log import PluginLog

# Supported video extensions
VIDEO_EXTS = (
    '.AVI', '.MPEG', '.MPG', '.WMV', '.ASF', '.FLV', '.MKV', '.QT', '.MP4', '.NUT', '.OGG', '.OGM', '.MOV',
    '.RAM', '.RM', '.RV', '.RMVB', '.3GP', '.VIVO', '.NUV', '.NSV', '.FLI', '.FLC', '.DVR-MS', '.WTV', '.TRP', '.F4V'
)


class VideoScanner(threading.Thread):
    def __init__(self, play_list: PlayListExtended, base_path):
        super().__init__()
        self.play_list = play_list
        self.daemon = True
        self.base_path = xbmcvfs.translatePath(base_path)
        self.running = True
        self.lock = threading.Lock()

    def run(self):
        PluginLog.info("scanner started")
        try:
            for root, _, files in os.walk(self.base_path, followlinks=True):
                if not self.running or xbmc.Monitor().abortRequested():
                    return

                for file in random.sample(files, len(files)):
                    if file.upper().endswith(VIDEO_EXTS):
                        path = os.path.join(root, file)
                        self.play_list.add_item(path)
        except Exception as e:
            PluginLog.error(f"scanner error: {str(e)}")
            time.sleep(10)
        PluginLog.info("scanner stopped")

    def stop(self):
        PluginLog.info("scanner stopping")
        self.running = False
