"""NFO Scanner - Scans video folders for movie.nfo and category.nfo files"""
import os
import time
import threading
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
import xbmc
import xbmcvfs

from .plugin_log import PluginLog


class FolderNode:
    """Represents a folder in the scanning tree"""
    def __init__(self, path: str, parent=None):
        self.path = path
        self.parent = parent
        self.children = {}
        self.scanned = False
        self.mtime = 0
        self.genres = set()  # Genres from category.nfo
        
    def add_child(self, name: str):
        """Add a child folder"""
        if name not in self.children:
            self.children[name] = FolderNode(os.path.join(self.path, name), self)
        return self.children[name]
    
    def mark_scanned(self):
        """Mark this folder as scanned"""
        self.scanned = True
        # If all children are scanned, we can compress memory by clearing children
        if self.children and all(child.scanned for child in self.children.values()):
            self.children.clear()


class NFOScanner:
    """Main NFO scanner class"""
    
    def __init__(self, addon, monitor):
        self.addon = addon
        self.monitor = monitor
        self.running = False
        self.paused = False
        self.scan_thread = None
        self.lock = threading.Lock()
        
        # Initialize plugin logger
        self.plugin_log = PluginLog(addon)
        
        # Folder tracking
        self.folder_tree = {}  # root path -> FolderNode
        self.priority_queue = []  # List of folders to scan with priority
        
        # Settings
        self.scan_interval = 60  # minutes
        self.thread_count = 1
        self.pause_on_playback = True
        self.debug_logging = False
        self.scan_network_sources = True
        
        self.load_settings()
    
    def log(self, msg: str, level=xbmc.LOGINFO):
        """Log message"""
        # Map xbmc log levels to plugin log levels
        if level == xbmc.LOGDEBUG:
            self.plugin_log.debug(msg)
        elif level == xbmc.LOGWARNING:
            self.plugin_log.warning(msg)
        elif level == xbmc.LOGERROR:
            self.plugin_log.error(msg)
        else:
            self.plugin_log.info(msg)
    
    def load_settings(self):
        """Load settings from addon configuration"""
        try:
            self.scan_interval = int(self.addon.getSetting('scan_interval'))
            self.thread_count = int(self.addon.getSetting('thread_count'))
            self.pause_on_playback = self.addon.getSetting('pause_on_playback') == 'true'
            self.debug_logging = self.addon.getSetting('debug_logging') == 'true'
            self.scan_network_sources = self.addon.getSetting('scan_network_sources') == 'true'
            
            # Update plugin log debug setting
            self.plugin_log.set_debug_enabled(self.debug_logging)
            
            self.log(f'Settings loaded: interval={self.scan_interval}min, threads={self.thread_count}')
        except Exception as e:
            self.log(f'Error loading settings: {e}', xbmc.LOGERROR)
    
    def get_video_sources(self) -> List[Dict]:
        """Get video sources from Kodi via JSON-RPC"""
        try:
            # Get movie sources
            request = json.dumps({
                "jsonrpc": "2.0",
                "method": "Files.GetSources",
                "params": {"media": "video"},
                "id": 1
            })
            response = xbmc.executeJSONRPC(request)
            result = json.loads(response)
            
            sources = []
            if 'result' in result and 'sources' in result['result']:
                for source in result['result']['sources']:
                    file_path = source.get('file', '')
                    # Filter network sources if needed
                    if not self.scan_network_sources:
                        if file_path.startswith(('smb://', 'nfs://', 'ftp://', 'http://', 'https://')):
                            continue
                    sources.append({
                        'path': xbmcvfs.translatePath(file_path),
                        'label': source.get('label', '')
                    })
            
            self.log(f'Found {len(sources)} video sources', xbmc.LOGDEBUG)
            return sources
        except Exception as e:
            self.log(f'Error getting video sources: {e}', xbmc.LOGERROR)
            return []
    
    def get_folder_mtime(self, path: str) -> float:
        """Get folder modification time"""
        try:
            stat = xbmcvfs.Stat(path)
            return stat.st_mtime()
        except:
            return 0
    
    def read_category_nfo(self, path: str) -> Set[str]:
        """Read genres from category.nfo file"""
        genres = set()
        category_path = os.path.join(path, 'category.nfo')
        
        try:
            if xbmcvfs.exists(category_path):
                file_obj = xbmcvfs.File(category_path, 'r')
                content = file_obj.read()
                file_obj.close()
                
                # Parse XML
                root = ET.fromstring(content)
                for genre_elem in root.findall('.//genre'):
                    if genre_elem.text:
                        genres.add(genre_elem.text.strip())
                
                self.log(f'Found genres in {category_path}: {genres}', xbmc.LOGDEBUG)
        except Exception as e:
            self.log(f'Error reading category.nfo from {path}: {e}', xbmc.LOGDEBUG)
        
        return genres
    
    def get_movie_nfo_mtime(self, path: str) -> float:
        """Get modification time of movie.nfo file"""
        nfo_path = os.path.join(path, 'movie.nfo')
        try:
            if xbmcvfs.exists(nfo_path):
                stat = xbmcvfs.Stat(nfo_path)
                return stat.st_mtime()
        except Exception:
            pass
        return 0
    
    def get_kodi_movie_date(self, path: str) -> float:
        """Get movie date from Kodi database via JSON-RPC"""
        try:
            # Query for movie by path
            request = json.dumps({
                "jsonrpc": "2.0",
                "method": "VideoLibrary.GetMovies",
                "params": {
                    "properties": ["file", "dateadded", "lastplayed"],
                    "filter": {
                        "field": "path",
                        "operator": "contains",
                        "value": path
                    }
                },
                "id": 1
            })
            response = xbmc.executeJSONRPC(request)
            result = json.loads(response)
            
            if 'result' in result and 'movies' in result['result'] and result['result']['movies']:
                movie = result['result']['movies'][0]
                # Parse dateadded to timestamp
                date_str = movie.get('dateadded', '')
                if date_str:
                    # Convert ISO format to timestamp
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    return dt.timestamp()
        except Exception as e:
            self.log(f'Error getting movie date from Kodi DB: {e}', xbmc.LOGDEBUG)
        
        return 0
    
    def reimport_movie(self, path: str, genres: Set[str]) -> bool:
        """Re-import movie.nfo into Kodi database"""
        try:
            self.log(f'Re-importing movie from: {path}', xbmc.LOGINFO)
            
            # Remove existing movie from library
            movie_id = self.get_movie_id_by_path(path)
            if movie_id is not None:
                request = json.dumps({
                    "jsonrpc": "2.0",
                    "method": "VideoLibrary.RemoveMovie",
                    "params": {
                        "movieid": movie_id
                    },
                    "id": 1
                })
                xbmc.executeJSONRPC(request)
            
            # Trigger scan of specific directory
            request = json.dumps({
                "jsonrpc": "2.0",
                "method": "VideoLibrary.Scan",
                "params": {
                    "directory": path,
                    "showdialogs": False
                },
                "id": 1
            })
            response = xbmc.executeJSONRPC(request)
            result = json.loads(response)
            
            # If we have additional genres from category.nfo, add them
            if genres:
                self.add_genres_to_movie(path, genres)
            
            self.log(f'Successfully re-imported: {path}', xbmc.LOGDEBUG)
            return 'result' in result
        except Exception as e:
            self.log(f'Error re-importing movie from {path}: {e}', xbmc.LOGERROR)
            return False
    
    def get_movie_id_by_path(self, path: str) -> Optional[int]:
        """Get movie ID from Kodi database by path"""
        try:
            request = json.dumps({
                "jsonrpc": "2.0",
                "method": "VideoLibrary.GetMovies",
                "params": {
                    "properties": ["file"],
                    "filter": {
                        "field": "path",
                        "operator": "contains",
                        "value": path
                    }
                },
                "id": 1
            })
            response = xbmc.executeJSONRPC(request)
            result = json.loads(response)
            
            if 'result' in result and 'movies' in result['result'] and result['result']['movies']:
                return result['result']['movies'][0].get('movieid')
        except Exception as e:
            self.log(f'Error getting movie ID: {e}', xbmc.LOGDEBUG)
        
        return None
    
    def add_genres_to_movie(self, path: str, genres: Set[str]):
        """Add genres from category.nfo to movie in Kodi database"""
        try:
            movie_id = self.get_movie_id_by_path(path)
            if not movie_id:
                return
            
            # Get current genres
            request = json.dumps({
                "jsonrpc": "2.0",
                "method": "VideoLibrary.GetMovieDetails",
                "params": {
                    "movieid": movie_id,
                    "properties": ["genre"]
                },
                "id": 1
            })
            response = xbmc.executeJSONRPC(request)
            result = json.loads(response)
            
            current_genres = set()
            if 'result' in result and 'moviedetails' in result['result']:
                current_genres = set(result['result']['moviedetails'].get('genre', []))
            
            # Merge genres
            all_genres = current_genres | genres
            
            # Update movie with new genres
            request = json.dumps({
                "jsonrpc": "2.0",
                "method": "VideoLibrary.SetMovieDetails",
                "params": {
                    "movieid": movie_id,
                    "genre": list(all_genres)
                },
                "id": 1
            })
            xbmc.executeJSONRPC(request)
            
            self.log(f'Added genres {genres} to movie at {path}', xbmc.LOGDEBUG)
        except Exception as e:
            self.log(f'Error adding genres to movie: {e}', xbmc.LOGDEBUG)
    
    def scan_folder(self, path: str, parent_genres: Set[str] = None) -> int:
        """Scan a folder for movie.nfo and category.nfo files"""
        if not self.running or self.monitor.abortRequested():
            return 0
        
        # Wait if paused
        while self.paused and self.running:
            if self.monitor.waitForAbort(1):
                return 0
        
        scanned_count = 0
        
        try:
            # Read category.nfo from current folder
            current_genres = self.read_category_nfo(path)
            # Merge with parent genres
            all_genres = (parent_genres or set()) | current_genres
            
            # Check if movie.nfo exists
            nfo_mtime = self.get_movie_nfo_mtime(path)
            if nfo_mtime > 0:
                # Check if we need to re-import
                kodi_date = self.get_kodi_movie_date(path)
                if nfo_mtime > kodi_date:
                    self.log(f'NFO newer than DB for {path}, re-importing', xbmc.LOGINFO)
                    if self.reimport_movie(path, all_genres):
                        scanned_count += 1
                elif all_genres and kodi_date > 0:
                    # Even if NFO is not newer, add genres from category.nfo
                    self.add_genres_to_movie(path, all_genres)
            
            # Scan subdirectories
            try:
                dirs, files = xbmcvfs.listdir(path)
                
                # Sort directories by modification time (newest first)
                dir_times = []
                for dir_name in dirs:
                    dir_path = os.path.join(path, dir_name)
                    mtime = self.get_folder_mtime(dir_path)
                    dir_times.append((mtime, dir_path))
                
                dir_times.sort(reverse=True)  # Newest first
                
                # Recursively scan subdirectories
                for _, dir_path in dir_times:
                    if not self.running or self.monitor.abortRequested():
                        break
                    scanned_count += self.scan_folder(dir_path, all_genres)
                    
            except Exception as e:
                self.log(f'Error listing directory {path}: {e}', xbmc.LOGDEBUG)
        
        except Exception as e:
            self.log(f'Error scanning folder {path}: {e}', xbmc.LOGERROR)
        
        return scanned_count
    
    def scan_all_sources(self):
        """Scan all video sources"""
        try:
            sources = self.get_video_sources()
            if not sources:
                self.log('No video sources found', xbmc.LOGWARNING)
                return
            
            self.log(f'Starting scan of {len(sources)} sources', xbmc.LOGINFO)
            
            total_scanned = 0
            for source in sources:
                if not self.running or self.monitor.abortRequested():
                    break
                
                path = source['path']
                label = source['label']
                self.log(f'Scanning source: {label} ({path})', xbmc.LOGINFO)
                
                try:
                    scanned = self.scan_folder(path)
                    total_scanned += scanned
                except Exception as e:
                    self.log(f'Error scanning source {label}: {e}', xbmc.LOGERROR)
            
            self.log(f'Scan completed. Re-imported {total_scanned} items', xbmc.LOGINFO)
            
        except Exception as e:
            self.log(f'Error during scan: {e}', xbmc.LOGERROR)
    
    def start(self):
        """Start the scanner"""
        with self.lock:
            if self.running:
                self.log('Scanner already running', xbmc.LOGWARNING)
                return
            
            self.running = True
            self.scan_thread = threading.Thread(target=self.run_scanner)
            self.scan_thread.daemon = True
            self.scan_thread.start()
            self.log('Scanner started', xbmc.LOGINFO)
    
    def stop(self):
        """Stop the scanner"""
        with self.lock:
            if not self.running:
                return
            
            self.running = False
            if self.scan_thread:
                self.scan_thread.join(timeout=5)
            self.log('Scanner stopped', xbmc.LOGINFO)
    
    def pause(self):
        """Pause the scanner"""
        self.paused = True
        self.log('Scanner paused', xbmc.LOGINFO)
    
    def resume(self):
        """Resume the scanner"""
        self.paused = False
        self.log('Scanner resumed', xbmc.LOGINFO)
    
    def clear_cache(self):
        """Clear the scanned folders cache"""
        with self.lock:
            self.folder_tree.clear()
            self.priority_queue.clear()
            self.log('Cache cleared', xbmc.LOGINFO)
    
    def add_priority_folder(self, path: str):
        """Add a folder to the priority queue for immediate scanning"""
        with self.lock:
            if path not in self.priority_queue:
                self.priority_queue.insert(0, path)
                self.log(f'Added priority folder: {path}', xbmc.LOGDEBUG)
    
    def run_scanner(self):
        """Main scanner loop"""
        last_scan_time = 0
        
        while self.running and not self.monitor.abortRequested():
            try:
                current_time = time.time()
                scan_interval_seconds = self.scan_interval * 60
                
                # Check if it's time to scan
                if current_time - last_scan_time >= scan_interval_seconds:
                    if not self.paused:
                        self.scan_all_sources()
                        last_scan_time = current_time
                
                # Wait a bit before checking again
                if self.monitor.waitForAbort(10):
                    break
                    
            except Exception as e:
                self.log(f'Error in scanner loop: {e}', xbmc.LOGERROR)
                if self.monitor.waitForAbort(30):
                    break
        
        self.log('Scanner loop ended', xbmc.LOGINFO)
