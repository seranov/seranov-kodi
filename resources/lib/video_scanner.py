import os
import threading
import time
import random
from queue import Queue
import xbmcvfs
import xbmc

# Supported video extensions
VIDEO_EXTS = (
    '.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.mpg', '.mpeg',
    '.m4v', '.3gp', '.ts', '.m2ts', '.divx', '.xvid'
)

class VideoScanner(threading.Thread):
    def __init__(self, base_path):
        super().__init__()
        self.daemon = True
        self.base_path = xbmcvfs.translatePath(base_path)
        self.found_videos = set()
        self.new_videos = Queue()
        self.running = True
        self.lock = threading.Lock()

    def run(self):
        while self.running and not xbmc.Monitor().abortRequested():
            try:
                current_videos = set()
                for root, _, files in os.walk(self.base_path):
                    if not self.running or xbmc.Monitor().abortRequested():
                        return

                    for file in files:
                        if file.lower().endswith(VIDEO_EXTS):
                            path = os.path.join(root, file)
                            current_videos.add(path)

                            if path not in self.found_videos:
                                self.new_videos.put(path)

                with self.lock:
                    self.found_videos = current_videos

                for _ in range(30):  # SCAN_INTERVAL
                    if not self.running or xbmc.Monitor().abortRequested():
                        return
                    time.sleep(1)

            except Exception as e:
                xbmc.log(f"Scanner error: {str(e)}", xbmc.LOGERROR)
                time.sleep(10)

    def stop(self):
        self.running = False

    def get_random_videos(self, count):
        with self.lock:
            if not self.found_videos:
                return []

            available = list(self.found_videos)
            count = min(count, len(available))
            return random.sample(available, count)