import os
import random
import time

import xbmcgui

from resources.lib.plugin_log import PluginLog


class PlayListExtended:
    def __init__(self):
        self.itemsAll = []
        self.itemsPlayed = []
        self.playlist = []
        self.lastPlayedIndex = -1
        self.lastUpdateTime = 0
        self.clear()

    @staticmethod
    def create_playlist_item(url):
        title = ' / '.join(reversed(url.split('/')))
        item = xbmcgui.ListItem(label=title, path=url)

        folder_path = os.path.dirname(url)
        folder_art_path = os.path.join(folder_path, "folder.jpg")
        if os.path.exists(folder_art_path):
            item.setArt({'icon': folder_art_path, 'poster': folder_art_path, 'thumb': folder_art_path})

        item.setInfo('video', {'title': title})
        item.setProperty('IsPlayable', 'true')
        item.setIsFolder(False)

        return item

    def get_item_count(self):
        PluginLog.debug(f"returning item count {len(self.itemsAll)}")
        return len(self.itemsAll)

    def get_last_update_time(self):
        return self.lastUpdateTime

    def getlast_played_index(self):
        return self.lastPlayedIndex

    def update_last_played_index(self, index):
        if index > self.lastPlayedIndex:
            self.lastPlayedIndex = index
            self.itemsPlayed = self.playlist[:self.lastPlayedIndex + 1]
            PluginLog.info(f"updated last played index: {self.lastPlayedIndex}")

    def add_item(self, item):
        self.itemsAll.append(PlayListExtended.create_playlist_item(item))
        self.lastUpdateTime = time.time()
        PluginLog.info(f"appended item: {item}; total count {len(self.itemsAll)}")

    def get_play_list(self):
        playlist_new = self.itemsPlayed[:]
        playlist_new.extend(random.sample(self.itemsAll, len(self.itemsAll)))
        playlist = playlist_new
        PluginLog.debug(f"generated playlist of size {len(playlist)} from played {len(self.itemsPlayed)} and all {len(self.itemsAll)}")
        return playlist

    def clear(self):
        PluginLog.info("clearing playlist")
        self.itemsAll.clear()
        self.itemsPlayed.clear()
        self.playlist.clear()
        self.lastPlayedIndex = -1
        self.lastUpdateTime = 0

    def __str__(self):
        return f"PlayListExtended(itemsAll={self.itemsAll}; itemsPlayed={self.itemsPlayed}; playlist={self.playlist})"
