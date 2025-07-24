import sys
import xbmc
import xbmcaddon
from urllib.parse import parse_qs

from xbmcgui import ListItem

from resources.lib.play_list import PlayListExtended
from resources.lib.plugin_log import PluginLog
from resources.lib.video_scanner import VideoScanner
from resources.lib.playback_manager import PlaybackManager
from resources.lib.player import PlayerWithEvents

addon = xbmcaddon.Addon()
monitor = xbmc.Monitor()
player = PlayerWithEvents()
play_list = PlayListExtended()


def start_playback(list_item: ListItem = None):
    playback_base_path = list_item.getPath()
    if not playback_base_path:
        PluginLog.info("no path")
        return
    else:
        PluginLog.info(f"path={playback_base_path}")

    play_list.clear()

    scanner = VideoScanner(play_list, playback_base_path)
    scanner.start()

    manager = PlaybackManager(play_list, monitor, player)
    player.set_playback_manager(manager)
    manager.manage_playback()

    scanner.stop()
    play_list.clear()


if __name__ == '__main__':
    args = sys.argv[1:]
    params = parse_qs(args[1]) if len(args) > 1 else {}
    # noinspection PyUnresolvedReferences
    PluginLog.info(f"args={args}; sys.listitem={sys.listitem}")

    # Check for context menu action
    if "play-random-recursive" in args:
        # noinspection PyUnresolvedReferences
        start_playback(sys.listitem)
    else:
        PluginLog.info("no valid context menu action")
