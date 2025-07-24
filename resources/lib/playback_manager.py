import time
import xbmc

from resources.lib.play_list import PlayListExtended
from resources.lib.plugin_log import PluginLog


class PlaybackManager:
    def __init__(self, play_list: PlayListExtended, monitor, player, playlist_size=20, min_start_videos=1):
        self.play_list = play_list
        self.monitor = monitor
        self.player = player
        self.playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        self.playlist_size = playlist_size
        self.min_start_videos = min_start_videos
        self.next_playlist = []
        self.lastUpdateTime = 0
        self.first_play = True
        self.running = True

    def manage_playback(self):
        while self.running and not self.monitor.abortRequested():
            try:
                if self.first_play:
                    self._initialize_playlist()
                    continue

                if self.player.isPlayingVideo():
                    self._handle_playback()
                else:
                    self._update_next_playlist()

            except Exception as e:
                PluginLog.error(f"error: {str(e)}")

            self.monitor.waitForAbort(1)
        PluginLog.info(f"aborted")

    def _initialize_playlist(self):
        PluginLog.info("_initialize_playlist")
        while self.play_list.get_un_played_count() < self.min_start_videos:
            if self.monitor.abortRequested():
                return
            self.monitor.waitForAbort(0.5)
        self._update_next_playlist()
        self.player.play(self.playlist)
        self.first_play = False

    def _handle_playback(self):
        if self.lastUpdateTime < self.play_list.get_last_update_time():
            self._update_next_playlist()

    def _update_next_playlist(self):
        PluginLog.info("_update_next_playlist")
        self.play_list.update_last_played_index(self.playlist.getposition())
        self._generate_next_playlist()
        self._replace_playlist()

    def _generate_next_playlist(self):
        PluginLog.info("_generate_next_playlist")
        self.next_playlist = self.play_list.get_play_list()
        self.last_update_time = time.time()

    def _replace_playlist(self):
        PluginLog.info("_replace_playlist")
        self.playlist.clear()
        for item in self.next_playlist:
            self.playlist.add(item.getPath(), item)
        self.next_playlist = []

    def stop(self):
        PluginLog.info("playback stopped")
        self.running = False
