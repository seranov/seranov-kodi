"""Log Viewer Script - Shows the scanner log in a text viewer"""
import sys
import xbmc
import xbmcaddon
import xbmcgui

# Import log manager
from resources.lib.plugin_log import PluginLog

# Get addon information
addon = xbmcaddon.Addon()


def show_log():
    """Display the log file in a text viewer dialog"""
    try:
        # Create log manager instance
        log_manager = PluginLog(addon)
        
        # Read the log file
        log_content = log_manager.read_log()
        
        # Show in a text viewer dialog
        dialog = xbmcgui.Dialog()
        dialog.textviewer(
            addon.getLocalizedString(32110),  # Scanner Log
            log_content
        )
        
    except Exception as e:
        xbmc.log(f'[{addon.getAddonInfo("id")}] Error showing log: {e}', xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            addon.getLocalizedString(32100),  # NFO Scanner
            f'Error loading log: {e}'
        )


def clear_log():
    """Clear the log file"""
    try:
        # Confirm with user
        dialog = xbmcgui.Dialog()
        if dialog.yesno(
            addon.getLocalizedString(32100),  # NFO Scanner
            addon.getLocalizedString(32111)   # Are you sure you want to clear the log?
        ):
            # Create log manager instance
            log_manager = PluginLog(addon)
            
            # Clear the log
            log_manager.clear_log()
            
            # Show confirmation
            dialog.ok(
                addon.getLocalizedString(32100),  # NFO Scanner
                addon.getLocalizedString(32112)   # Log cleared successfully
            )
    
    except Exception as e:
        xbmc.log(f'[{addon.getAddonInfo("id")}] Error clearing log: {e}', xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            addon.getLocalizedString(32100),  # NFO Scanner
            f'Error clearing log: {e}'
        )


def handle_action():
    """Handle command line action"""
    if len(sys.argv) > 1:
        action = None
        for arg in sys.argv[1:]:
            if arg.startswith('action='):
                action = arg.split('=', 1)[1]
        
        if action == 'view_log':
            show_log()
        elif action == 'clear_log':
            clear_log()
        else:
            xbmc.log(f'[{addon.getAddonInfo("id")}] Unknown action: {action}', xbmc.LOGWARNING)
    else:
        # Default action is to show log
        show_log()


if __name__ == '__main__':
    handle_action()
