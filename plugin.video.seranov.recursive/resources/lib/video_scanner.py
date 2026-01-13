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
        self.visited = set()

    def scan_folder(self, folder):
        if not self.running or xbmc.Monitor().abortRequested():
            return
        real_path = os.path.realpath(folder)
        if real_path in self.visited:
            return
        self.visited.add(real_path)
        items = os.listdir(real_path)
        random.shuffle(items)
        for item in items:
            path = os.path.join(folder, item)
            if os.path.isdir(path):
                self.scan_folder(path)
            else:
                if item.upper().endswith(VIDEO_EXTS):
                    self.play_list.add_item(path)

    def run(self):
        PluginLog.info("scanner started")
        try:
            self.visited.clear()
            self.scan_folder(self.base_path)
        except Exception as e:
            PluginLog.error(f"scanner error: {str(e)}")
            time.sleep(10)
        PluginLog.info("scanner stopped")

    def stop(self):
        PluginLog.info("scanner stopping")
        self.running = False
