"""Plugin Log Manager - Handles file-based logging for NFO Scanner"""
import os
import time
from datetime import datetime
from typing import Optional
import xbmc
import xbmcvfs


class PluginLog:
    """Manages plugin logging to a file"""
    
    # Log levels
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    
    LEVEL_NAMES = {
        DEBUG: 'DEBUG',
        INFO: 'INFO',
        WARNING: 'WARNING',
        ERROR: 'ERROR'
    }
    
    def __init__(self, addon, max_size_mb: int = 2, max_lines: int = 1000):
        """
        Initialize the plugin logger
        
        Args:
            addon: The Kodi addon instance
            max_size_mb: Maximum log file size in MB before rotation
            max_lines: Maximum number of lines to keep in log
        """
        self.addon = addon
        self.addon_id = addon.getAddonInfo('id')
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_lines = max_lines
        
        # Get addon data directory
        profile_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
        if not xbmcvfs.exists(profile_path):
            xbmcvfs.mkdirs(profile_path)
        
        self.log_file = os.path.join(profile_path, 'scanner.log')
        self.debug_enabled = False
        
        # Log to Kodi log that we're using file-based logging
        xbmc.log(f'[{self.addon_id}] Plugin log file: {self.log_file}', xbmc.LOGINFO)
    
    def set_debug_enabled(self, enabled: bool):
        """Enable or disable debug logging"""
        self.debug_enabled = enabled
    
    def _write_to_file(self, message: str):
        """Write message to log file with rotation"""
        try:
            # Check if rotation is needed
            if xbmcvfs.exists(self.log_file):
                stat = xbmcvfs.Stat(self.log_file)
                if stat.st_size() > self.max_size_bytes:
                    self._rotate_log()
            
            # Append to log file
            file_obj = xbmcvfs.File(self.log_file, 'a')
            file_obj.write(message.encode('utf-8') + b'\n')
            file_obj.close()
            
        except Exception as e:
            # If file logging fails, at least log to Kodi log
            xbmc.log(f'[{self.addon_id}] Error writing to log file: {e}', xbmc.LOGERROR)
    
    def _rotate_log(self):
        """Rotate log file by keeping only recent entries"""
        try:
            # Read existing log
            file_obj = xbmcvfs.File(self.log_file, 'r')
            content = file_obj.read()
            file_obj.close()
            
            # Decode and split into lines
            lines = content.decode('utf-8', errors='ignore').split('\n')
            
            # Keep only last N lines
            if len(lines) > self.max_lines:
                lines = lines[-self.max_lines:]
            
            # Write back
            file_obj = xbmcvfs.File(self.log_file, 'w')
            file_obj.write('\n'.join(lines).encode('utf-8'))
            file_obj.close()
            
            xbmc.log(f'[{self.addon_id}] Log file rotated', xbmc.LOGINFO)
            
        except Exception as e:
            xbmc.log(f'[{self.addon_id}] Error rotating log file: {e}', xbmc.LOGERROR)
    
    def log(self, message: str, level: int = INFO):
        """
        Log a message
        
        Args:
            message: The message to log
            level: Log level (DEBUG, INFO, WARNING, ERROR)
        """
        # Skip debug messages if debug is not enabled
        if level == self.DEBUG and not self.debug_enabled:
            return
        
        # Create timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        level_name = self.LEVEL_NAMES.get(level, 'INFO')
        
        # Format message
        log_message = f'[{timestamp}] [{level_name}] {message}'
        
        # Write to file
        self._write_to_file(log_message)
        
        # Also write to Kodi log for errors and warnings
        if level >= self.WARNING:
            kodi_level = xbmc.LOGERROR if level == self.ERROR else xbmc.LOGWARNING
            xbmc.log(f'[{self.addon_id}] {message}', kodi_level)
    
    def debug(self, message: str):
        """Log a debug message"""
        self.log(message, self.DEBUG)
    
    def info(self, message: str):
        """Log an info message"""
        self.log(message, self.INFO)
    
    def warning(self, message: str):
        """Log a warning message"""
        self.log(message, self.WARNING)
    
    def error(self, message: str):
        """Log an error message"""
        self.log(message, self.ERROR)
    
    def get_log_path(self) -> str:
        """Get the path to the log file"""
        return self.log_file
    
    def clear_log(self):
        """Clear the log file"""
        try:
            if xbmcvfs.exists(self.log_file):
                xbmcvfs.delete(self.log_file)
                self.info('Log file cleared')
                xbmc.log(f'[{self.addon_id}] Log file cleared', xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f'[{self.addon_id}] Error clearing log file: {e}', xbmc.LOGERROR)
    
    def read_log(self, max_lines: Optional[int] = None) -> str:
        """
        Read the log file content
        
        Args:
            max_lines: Maximum number of lines to return (from end)
        
        Returns:
            Log file content as string
        """
        try:
            if not xbmcvfs.exists(self.log_file):
                return 'No log file exists yet.'
            
            file_obj = xbmcvfs.File(self.log_file, 'r')
            content = file_obj.read()
            file_obj.close()
            
            # Decode content
            text = content.decode('utf-8', errors='ignore')
            
            # Limit lines if requested
            if max_lines:
                lines = text.split('\n')
                if len(lines) > max_lines:
                    lines = lines[-max_lines:]
                text = '\n'.join(lines)
            
            return text
            
        except Exception as e:
            error_msg = f'Error reading log file: {e}'
            xbmc.log(f'[{self.addon_id}] {error_msg}', xbmc.LOGERROR)
            return error_msg
