import time
import random
import xbmc
import xbmcgui
import xbmcaddon
from queue import Empty
from resources.lib.video_scanner import VideoScanner

class PlaybackManager:
    def __init__(self, scanner, monitor, player, playlist_size=20, min_start_videos=3):
        self.scanner = scanner
        self.monitor = monitor
        self.player = player
        self.playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        self.playlist_size = playlist_size
        self.min_start_videos = min_start_videos
        self.next_playlist = []
        self.last_update_time = 0
        self.first_play = True

    def create_playlist_item(self, video_path):
        """Creates a playlist item with proper metadata."""
        item = xbmcgui.ListItem(path=video_path)
        item.setInfo('video', {'title': video_path.split('/')[-1]})
        item.setProperty('IsPlayable', 'true')
        return item

    def manage_playback(self):
        """Main playback management loop."""
        while not self.monitor.abortRequested():
            try:
                if self.first_play:
                    self._initialize_playlist()
                    continue

                if self.player.isPlayingVideo():
                    self._handle_playback()
                else:
                    self._update_next_playlist()

            except Exception as e:
                xbmc.log(f"Playback manager error: {str(e)}", xbmc.LOGERROR)

            self.monitor.waitForAbort(1)

    def _initialize_playlist(self):
        """Initializes the playlist on the first run."""
        while self.scanner.new_videos.qsize() < self.min_start_videos:
            if self.monitor.abortRequested():
                return
            self.monitor.waitForAbort(0.5)

        initial_videos = []
        while not self.scanner.new_videos.empty():
            initial_videos.append(self.scanner.new_videos.get())

        random.shuffle(initial_videos)
        self.playlist.clear()

        for video in initial_videos:
            self.playlist.add(video, self.create_playlist_item(video))

        self.player.play(self.playlist)
        self.first_play = False

    def _handle_playback(self):
        """Handles playback and playlist updates."""
        current_idx = self.playlist.getposition()
        total_items = self.playlist.size()

        if total_items - current_idx <= 1:
            if not self.next_playlist or time.time() - self.last_update_time > 30:
                self._generate_next_playlist()

            self._replace_playlist()

    def _update_next_playlist(self):
        """Periodically updates the next playlist in the background."""
        if not self.next_playlist or time.time() - self.last_update_time > 30:
            self._generate_next_playlist()

    def _generate_next_playlist(self):
        """Generates the next playlist."""
        self.next_playlist = [
            self.create_playlist_item(v)
            for v in self.scanner.get_random_videos(self.playlist_size)
        ]
        self.last_update_time = time.time()

    def _replace_playlist(self):
        """Replaces the current playlist with the next one."""
        self.playlist.lock()
        try:
            self.playlist.clear()
            for item in self.next_playlist:
                self.playlist.add(item.getfilename(), item)
        finally:
            self.playlist.unlock()

        self.next_playlist = []