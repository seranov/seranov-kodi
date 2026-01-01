import xbmc
import xbmcaddon

# Get addon information
addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo('id')
addon_name = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')

# Create monitor object
monitor = xbmc.Monitor()


def log(msg):
    """Log message to Kodi log"""
    xbmc.log(f'[{addon_id}] {msg}', xbmc.LOGINFO)


class ServiceTemplate1:
    """Main service class"""
    
    def __init__(self):
        self.running = True
        log(f'{addon_name} v{addon_version} started')
    
    def run(self):
        """Main service loop"""
        # Check interval from settings (in seconds)
        check_interval = int(addon.getSetting('check_interval'))
        
        while self.running and not monitor.abortRequested():
            # Wait for abort or timeout
            if monitor.waitForAbort(check_interval):
                # Abort was requested while waiting
                self.running = False
                break
            
            # Do service work here
            self.do_service_work()
        
        log(f'{addon_name} stopped')
    
    def do_service_work(self):
        """Perform the main service work"""
        # This is where you would implement your service logic
        # For template purposes, we just log that we're running
        log('Service is running...')
    
    def stop(self):
        """Stop the service"""
        self.running = False


if __name__ == '__main__':
    service = ServiceTemplate1()
    service.run()
