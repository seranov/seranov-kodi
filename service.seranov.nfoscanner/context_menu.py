"""Context menu script for NFO Scanner - Scan folder manually"""
import sys
import xbmc
import xbmcaddon
import xbmcgui

# Import scanner
from resources.lib.nfo_scanner import NFOScanner


def log(msg, level=xbmc.LOGINFO):
    """Log message to Kodi log"""
    addon_id = 'service.seranov.nfoscanner'
    xbmc.log(f'[{addon_id}] {msg}', level)


def scan_folder_manually():
    """Scan the selected folder manually"""
    try:
        # Get addon
        addon = xbmcaddon.Addon()
        
        # Get the folder path from the list item
        # Note: sys.listitem is a Kodi-specific attribute added by Kodi when running context menu scripts
        if hasattr(sys, 'listitem') and sys.listitem:
            folder_path = sys.listitem.getPath()
        else:
            log('No listitem available')
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # "NFO Scanner"
                addon.getLocalizedString(32120),  # "No folder selected"
                xbmcgui.NOTIFICATION_ERROR,
                5000
            )
            return
        
        if not folder_path:
            log('Empty folder path')
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # "NFO Scanner"
                addon.getLocalizedString(32120),  # "No folder selected"
                xbmcgui.NOTIFICATION_ERROR,
                5000
            )
            return
        
        log(f'Manual scan requested for folder: {folder_path}')
        
        # Show progress dialog
        progress = xbmcgui.DialogProgress()
        progress.create(
            addon.getLocalizedString(32100),  # "NFO Scanner"
            addon.getLocalizedString(32121)   # "Scanning folder..."
        )
        
        try:
            # Create a monitor for abort checking
            monitor = xbmc.Monitor()
            
            # Create scanner instance
            scanner = NFOScanner(addon, monitor)
            
            # Set scanner to running state for manual scan
            scanner.running = True
            
            # Scan the folder
            scanned_count = scanner.scan_folder(folder_path)
            
            # Show notification with result
            if scanned_count > 0:
                message = addon.getLocalizedString(32122).format(scanned_count)  # "Scanned {0} items"
            else:
                message = addon.getLocalizedString(32123)  # "No items needed updating"
            
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # "NFO Scanner"
                message,
                xbmcgui.NOTIFICATION_INFO,
                5000
            )
            
            log(f'Manual scan completed: {scanned_count} items processed')
            
        except Exception as e:
            log(f'Error during scan: {e}', xbmc.LOGERROR)
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # "NFO Scanner"
                addon.getLocalizedString(32107),  # "Error during scan"
                xbmcgui.NOTIFICATION_ERROR,
                5000
            )
        finally:
            # Always close progress dialog
            progress.close()
    
    except Exception as e:
        log(f'Error in context menu: {e}', xbmc.LOGERROR)


if __name__ == '__main__':
    scan_folder_manually()
