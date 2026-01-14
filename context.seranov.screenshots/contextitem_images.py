"""Context menu entry point for SeraNov Popup Screenshots"""
import sys
import xbmc
import xbmcaddon

from resources.lib.fs import FS
from resources.lib.ui import UI


def log(msg, level=xbmc.LOGINFO):
    """Log message to Kodi log"""
    addon_id = 'context.seranov.screenshots'
    xbmc.log(f'[{addon_id}] {msg}', level)


if __name__ == '__main__':
    try:
        log('=' * 60)
        log('CONTEXT MENU INVOKED')

        # Log addon info
        addon = xbmcaddon.Addon()
        log(f'Addon version: {addon.getAddonInfo("version")}')

        # Log settings
        context_menu_root = addon.getSetting('context_menu_root')
        context_menu_seranov = addon.getSetting('context_menu_seranov')
        log(f'Settings: root={context_menu_root}, seranov={context_menu_seranov}')

        # Log sys.argv
        log(f'sys.argv: {sys.argv}')

        # Get the list item that was right-clicked
        if hasattr(sys, 'listitem') and sys.listitem:
            list_item = sys.listitem
            path = list_item.getPath()
            log(f'Context menu invoked for path: {path}')

            fs = FS(list_item)
            ui = UI(fs)
            ui.slide_show_open()

            log('Slideshow completed successfully')
        else:
            log('No listitem available', xbmc.LOGWARNING)
            import xbmcgui
            xbmcgui.Dialog().notification(
                'Screenshots Error',
                'No item selected',
                xbmcgui.NOTIFICATION_WARNING,
                3000
            )

        log('=' * 60)

    except Exception as e:
        log(f'Context menu error: {e}', xbmc.LOGERROR)
        import traceback
        log(traceback.format_exc(), xbmc.LOGERROR)
