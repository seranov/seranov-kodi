import xbmc
import xbmcgui

from resources.lib.plugin_log import PluginLog


class PlayerWithEvents(xbmc.Player):
    def __init__(self, *args, **kwargs):
        self.playback_manager = kwargs.pop('playback_manager', None)
        super(PlayerWithEvents, self).__init__(*args, **kwargs)

    def set_playback_manager(self, playback_manager):
        self.playback_manager = playback_manager

    def onPlayBackStopped(self):
        PluginLog.info("onPlayBackStopped")
        if self.playback_manager:
            self.playback_manager.stop()
        super(PlayerWithEvents, self).onPlayBackStopped()

    def onPlayBackError(self):
        PluginLog.info("onPlayBackError")
        super(PlayerWithEvents, self).onPlayBackError()
        self.playnext()

