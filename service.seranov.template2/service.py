import xbmc
import xbmcaddon
import json

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
        self.service.load_settings()
    
    def onNotification(self, sender, method, data):
        """Called when a notification is received"""
        log(f'Notification received: {method}')
        
        # Handle different notification types
        if method == 'Player.OnPlay':
            self.service.on_playback_started()
        elif method == 'Player.OnStop':
            self.service.on_playback_stopped()


class ServiceTemplate2:
    """Main service class with event monitoring"""
    
    def __init__(self):
        self.running = True
        self.monitor = ServiceMonitor(self)
        log(f'{addon_name} v{addon_version} started')
        self.load_settings()
    
    def load_settings(self):
        """Load settings from addon configuration"""
        self.enable_playback_monitoring = addon.getSetting('enable_playback_monitoring') == 'true'
        self.enable_notifications = addon.getSetting('enable_notifications') == 'true'
        log(f'Settings loaded: playback_monitoring={self.enable_playback_monitoring}, notifications={self.enable_notifications}')
    
    def run(self):
        """Main service loop"""
        while self.running and not self.monitor.abortRequested():
            # Wait for abort (check every 1 second)
            if self.monitor.waitForAbort(1):
                # Abort was requested while waiting
                self.running = False
                break
        
        log(f'{addon_name} stopped')
    
    def on_playback_started(self):
        """Called when playback starts"""
        if self.enable_playback_monitoring:
            log('Playback started')
            # Add your custom logic here
    
    def on_playback_stopped(self):
        """Called when playback stops"""
        if self.enable_playback_monitoring:
            log('Playback stopped')
            # Add your custom logic here
    
    def stop(self):
        """Stop the service"""
        self.running = False


if __name__ == '__main__':
    service = ServiceTemplate2()
    service.run()
