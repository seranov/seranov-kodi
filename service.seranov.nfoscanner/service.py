"""NFO Scanner Service - Main service entry point"""
import sys
import xbmc
import xbmcaddon
import xbmcgui

# Import scanner
from resources.lib.nfo_scanner import NFOScanner

# Get addon information
addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo('id')
addon_name = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')


def log(msg):
    """Log message to Kodi log"""
    xbmc.log(f'[{addon_id}] {msg}', xbmc.LOGINFO)


class ServiceMonitor(xbmc.Monitor):
    """Custom monitor class to handle Kodi events"""
    
    def __init__(self, service):
        super().__init__()
        self.service = service
        log('Monitor initialized')
    
    def onSettingsChanged(self):
        """Called when addon settings are changed"""
        log('Settings changed, reloading...')
        if self.service.scanner:
            self.service.scanner.load_settings()
    
    def onNotification(self, sender, method, data):
        """Called when a notification is received"""
        # Handle playback events
        if method == 'Player.OnPlay':
            self.service.on_playback_started()
        elif method == 'Player.OnStop':
            self.service.on_playback_stopped()
        elif method == 'GUI.OnScreensaverActivated':
            # Could use this to trigger scanning during idle time
            pass
        elif method == 'Other.FolderChanged':
            # Track folder navigation for priority scanning
            try:
                import json
                folder_data = json.loads(data)
                folder_path = folder_data.get('path', '')
                if folder_path:
                    self.service.on_folder_navigation(folder_path)
            except:
                pass


class NFOScannerService:
    """Main service class"""
    
    def __init__(self):
        self.running = True
        self.monitor = ServiceMonitor(self)
        self.scanner = None
        
        log(f'{addon_name} v{addon_version} started')
        
        # Check if service is enabled
        self.enabled = addon.getSetting('enable_service') == 'true'
        
        if self.enabled:
            self.scanner = NFOScanner(addon, self.monitor)
            self.scanner.start()
        else:
            log('Service is disabled in settings')
    
    def run(self):
        """Main service loop"""
        # Handle command line arguments for manual control
        if len(sys.argv) > 1:
            self.handle_command(sys.argv[1:])
            return
        
        # Main loop
        while self.running and not self.monitor.abortRequested():
            # Wait for abort (check every 1 second)
            if self.monitor.waitForAbort(1):
                self.running = False
                break
        
        # Cleanup
        if self.scanner:
            self.scanner.stop()
        
        log(f'{addon_name} stopped')
    
    def handle_command(self, args):
        """Handle command line arguments"""
        if not args:
            return
        
        action = None
        for arg in args:
            if arg.startswith('action='):
                action = arg.split('=', 1)[1]
        
        if action == 'scan':
            self.manual_scan()
        elif action == 'stop':
            self.stop_scan()
        elif action == 'clear':
            self.clear_cache()
    
    def manual_scan(self):
        """Start a manual scan"""
        log('Manual scan requested')
        
        if not self.scanner:
            self.scanner = NFOScanner(addon, self.monitor)
        
        if not self.scanner.running:
            self.scanner.start()
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # NFO Scanner
                addon.getLocalizedString(32101),  # Scanning started
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
        else:
            # If already running, trigger immediate scan
            self.scanner.scan_all_sources()
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # NFO Scanner
                addon.getLocalizedString(32101),  # Scanning started
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
    
    def stop_scan(self):
        """Stop the scanner"""
        log('Stop scan requested')
        
        if self.scanner:
            self.scanner.stop()
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # NFO Scanner
                addon.getLocalizedString(32102),  # Scanning stopped
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
    
    def clear_cache(self):
        """Clear the scanner cache"""
        log('Clear cache requested')
        
        if self.scanner:
            self.scanner.clear_cache()
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # NFO Scanner
                addon.getLocalizedString(32105),  # Cache cleared
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
    
    def on_playback_started(self):
        """Called when playback starts"""
        if self.scanner and self.scanner.pause_on_playback:
            log('Playback started, pausing scanner')
            self.scanner.pause()
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # NFO Scanner
                addon.getLocalizedString(32103),  # Scanning paused (playback active)
                xbmcgui.NOTIFICATION_INFO,
                2000
            )
    
    def on_playback_stopped(self):
        """Called when playback stops"""
        if self.scanner and self.scanner.pause_on_playback:
            log('Playback stopped, resuming scanner')
            self.scanner.resume()
            xbmcgui.Dialog().notification(
                addon.getLocalizedString(32100),  # NFO Scanner
                addon.getLocalizedString(32104),  # Scanning resumed
                xbmcgui.NOTIFICATION_INFO,
                2000
            )
    
    def on_folder_navigation(self, folder_path: str):
        """Called when user navigates to a folder"""
        if self.scanner:
            log(f'User navigated to folder: {folder_path}')
            self.scanner.add_priority_folder(folder_path)


if __name__ == '__main__':
    service = NFOScannerService()
    service.run()
