import time
import xbmc

from resources.lib.play_list import PlayListExtended
from resources.lib.plugin_log import PluginLog


class PlaybackManager:
    def __init__(self, play_list: PlayListExtended, monitor, player):
        self.play_list = play_list
        self.monitor = monitor
        self.player = player
        self.playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        self.next_playlist = []
        self.lastUpdateTime = 0
        self.running = True

    def manage_playback(self):
        while self.running and not self.monitor.abortRequested():
            try:
                if self.playlist.size() < 1:
                    self._initialize_playlist()
                elif self.player.isPlayingVideo():
                    self._handle_playback()
                else:
                    self._update_next_playlist()
            except Exception as e:
                PluginLog.error(f"manage_playback error: {str(e)}")
            self.monitor.waitForAbort(1)
        PluginLog.info(f"manage_playback aborted")

    def _initialize_playlist(self):
        PluginLog.info("manage_playback _initialize_playlist")
        while self.play_list.get_item_count() < 1:
            if self.monitor.abortRequested():
                return
            self.monitor.waitForAbort(0.5)
        self._update_next_playlist()
        self.player.play(self.playlist)
        self.first_play = False

    def _handle_playback(self):
        if (self.lastUpdateTime < self.play_list.get_last_update_time()
                or self.playlist.getposition() >= self.playlist.size() - 1):
            self._update_next_playlist()

    def _update_next_playlist(self):
        PluginLog.info("manage_playback _update_next_playlist")
        self.play_list.update_last_played_index(self.playlist.getposition())
        self._generate_next_playlist()
        self._replace_playlist()

    def _generate_next_playlist(self):
        PluginLog.info("manage_playback _generate_next_playlist")
        self.next_playlist = self.play_list.get_play_list()
        self.last_update_time = time.time()

    def _replace_playlist(self):
        if len(self.next_playlist) > self.playlist.size():
            PluginLog.info("manage_playback _replace_playlist")
            self.playlist.clear()
            for item in self.next_playlist:
                self.playlist.add(item.getPath(), item)

    def stop(self):
        PluginLog.info("manage_playback stop")
        self.running = False
