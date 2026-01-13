"""Context menu entry point for Unified Video Browser"""
import sys
import xbmc
import xbmcaddon
import xbmcgui

def log(msg, level=xbmc.LOGINFO):
    """Log message"""
    xbmc.log(f'[UnifiedBrowser-Context] {msg}', level)

if __name__ == '__main__':
    try:
        addon = xbmcaddon.Addon()
        
        # Get the list item that was right-clicked
        # noinspection PyUnresolvedReferences
        list_item = sys.listitem
        
        if list_item:
            path = list_item.getPath()
            log(f'Context menu invoked for path: {path}')
        
        # Open the plugin
        plugin_url = 'plugin://plugin.video.seranov.browser/'
        xbmc.executebuiltin(f'ActivateWindow(Videos,{plugin_url},return)')
        
    except Exception as e:
        log(f'Context menu error: {e}', xbmc.LOGERROR)
        import traceback
        log(traceback.format_exc(), xbmc.LOGERROR)
