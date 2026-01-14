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
        log('=' * 60)
        log('CONTEXT MENU INVOKED')

        addon = xbmcaddon.Addon()
        log(f'Addon version: {addon.getAddonInfo("version")}')

        # Log settings
        context_menu_root = addon.getSetting('context_menu_root')
        context_menu_seranov = addon.getSetting('context_menu_seranov')
        log(f'Settings: root={context_menu_root}, seranov={context_menu_seranov}')

        # Log sys.argv
        log(f'sys.argv: {sys.argv}')

        # Get the list item that was right-clicked (optional)
        try:
            list_item = sys.listitem
            if list_item:
                path = list_item.getPath()
                log(f'Context menu invoked for path: {path}')
        except AttributeError:
            # sys.listitem may not be available in all contexts
            log('Context menu invoked without list item')
        
        # Open the plugin
        plugin_url = 'plugin://plugin.video.seranov.browser/'
        log(f'Opening plugin: {plugin_url}')
        xbmc.executebuiltin(f'ActivateWindow(Videos,{plugin_url},return)')
        
        log('Plugin opened successfully')
        log('=' * 60)

    except Exception as e:
        log(f'Context menu error: {e}', xbmc.LOGERROR)
        import traceback
        log(traceback.format_exc(), xbmc.LOGERROR)
