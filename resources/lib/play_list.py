import random
import time

import xbmcgui

from resources.lib.plugin_log import PluginLog


class PlayListExtended:
    def __init__(self):
        self.itemsAll = []
        self.itemsPlayed = []
        self.itemsUnPlayed = []
        self.lastPlayedIndex = -1
        self.lastUpdateTime = 0
        self.clear()

    def create_playlist_item(self, video_path):
        item = xbmcgui.ListItem(path=video_path)
        item.getVideoInfoTag().setTitle(video_path.split('/')[-1])
        item.setProperty('IsPlayable', 'true')
        item.setIsFolder(False)
        return item

    def get_last_update_time(self):
        return self.lastUpdateTime

    def getlast_played_index(self):
        return self.lastPlayedIndex

    def update_last_played_index(self, index):
        if 0 <= index < len(self.itemsAll):
            if self.lastPlayedIndex < index:
                self.lastPlayedIndex = index
                PluginLog.info(f"updated last played index: {self.lastPlayedIndex}")
                self.itemsPlayed = self.itemsAll[:self.lastPlayedIndex + 1]

    def get_un_played_count(self):
        return len(self.itemsAll) - len(self.itemsPlayed)

    def add_item(self, item):
        self.itemsAll.append(self.create_playlist_item(item))
        self.lastUpdateTime = time.time()
        PluginLog.info(f"appended item: {item}")

    def get_play_list(self):
        playlist = []
        un_played_items = self.itemsAll[len(self.itemsPlayed):]
        randomized_items = random.sample(un_played_items, len(un_played_items))
        for item in randomized_items:
            PluginLog.debug(f"before add item={item}")
            playlist.append(item)
        return playlist

    def clear(self):
        PluginLog.info("clearing playlist")
        self.itemsAll.clear()
        self.itemsPlayed.clear()
        self.itemsUnPlayed.clear()
        self.lastPlayedIndex = -1
        self.lastUpdateTime = 0

    def __str__(self):
        return f"PlayListExtended(itemsAll={self.itemsAll}; itemsPlayed={self.itemsPlayed})"
