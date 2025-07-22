import sys
import xbmc
import xbmcaddon
from urllib.parse import parse_qs
from resources.lib.video_scanner import VideoScanner
from resources.lib.playback_manager import PlaybackManager

addon = xbmcaddon.Addon()
monitor = xbmc.Monitor()
player = xbmc.Player()

def start_playback(playback_base_path):
    scanner = VideoScanner(playback_base_path)
    scanner.start()

    manager = PlaybackManager(scanner, monitor, player)
    manager.manage_playback()

    scanner.stop()
    xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()

if __name__ == '__main__':
    # Parse arguments
    args = sys.argv[1:]
    params = parse_qs(args[1]) if len(args) > 1 else {}

    # Check for context menu action
    if "context" in args and "root" in params:
        base_path = params["root"][0]
    else:
        base_path = addon.getSetting('target_dir') or 'special://home/'

    start_playback(base_path)