"""NFO Scanner - Scans video folders for movie.nfo and category.nfo files"""
import os
import time
import threading
import json
import xml.etree.ElementTree as ET
import traceback
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
            # Load settings with default values if empty
            scan_interval_str = self.addon.getSetting('scan_interval')
            self.scan_interval = int(scan_interval_str) if scan_interval_str else 60

            thread_count_str = self.addon.getSetting('thread_count')
            self.thread_count = int(thread_count_str) if thread_count_str else 1

            self.pause_on_playback = self.addon.getSetting('pause_on_playback') == 'true'
            self.debug_logging = self.addon.getSetting('debug_logging') == 'true'
            self.scan_network_sources = self.addon.getSetting('scan_network_sources') == 'true'
            
            # Update plugin log debug setting
            self.plugin_log.set_debug_enabled(self.debug_logging)
            
            self.log(f'Settings loaded: interval={self.scan_interval}min, threads={self.thread_count}, '
                    f'pause_on_playback={self.pause_on_playback}, debug_logging={self.debug_logging}, '
                    f'scan_network_sources={self.scan_network_sources}')
        except Exception as e:
            self.log(f'Error loading settings: {e}', xbmc.LOGERROR)
            self.log(f'Settings loading traceback: {traceback.format_exc()}', xbmc.LOGERROR)
    
    def get_video_sources(self) -> List[Dict]:
        """Get video sources from Kodi via JSON-RPC"""
        try:
            self.log('Requesting video sources from Kodi...', xbmc.LOGDEBUG)
            
            # Get movie sources
            request = json.dumps({
                "jsonrpc": "2.0",
                "method": "Files.GetSources",
                "params": {"media": "video"},
                "id": 1
            })
            
            self.log(f'JSON-RPC Request: {request}', xbmc.LOGDEBUG)
            response = xbmc.executeJSONRPC(request)
            self.log(f'JSON-RPC Response: {response}', xbmc.LOGDEBUG)
            
            result = json.loads(response)
            
            sources = []
            if 'result' in result and 'sources' in result['result']:
                for source in result['result']['sources']:
                    file_path = source.get('file', '')
                    label = source.get('label', '')
                    
                    # Filter network sources if needed
                    if not self.scan_network_sources:
                        if file_path.startswith(('smb://', 'nfs://', 'ftp://', 'http://', 'https://')):
                            self.log(f'Skipping network source: {label} ({file_path})', xbmc.LOGDEBUG)
                            continue
                    
                    translated_path = xbmcvfs.translatePath(file_path)
                    sources.append({
                        'path': translated_path,
                        'label': label
                    })
                    self.log(f'Added video source: {label} ({file_path} -> {translated_path})', xbmc.LOGDEBUG)
            
            self.log(f'Found {len(sources)} video sources to scan', xbmc.LOGINFO)
            return sources
        except Exception as e:
            self.log(f'Error getting video sources: {e}', xbmc.LOGERROR)
            self.log(f'Video sources error traceback: {traceback.format_exc()}', xbmc.LOGERROR)
            return []
    
    def get_folder_mtime(self, path: str) -> float:
        """Get folder modification time"""
        try:
            stat = xbmcvfs.Stat(path)
            mtime = stat.st_mtime()
            self.log(f'Folder mtime for {path}: {mtime} ({datetime.fromtimestamp(mtime)})', xbmc.LOGDEBUG)
            return mtime
        except Exception as e:
            self.log(f'Error getting folder mtime for {path}: {e}', xbmc.LOGDEBUG)
            self.log(f'Folder mtime error traceback: {traceback.format_exc()}', xbmc.LOGDEBUG)
            return 0
    
    def read_category_nfo(self, path: str) -> Set[str]:
        """Read genres from category.nfo file"""
        genres = set()
        category_path = os.path.join(path, 'category.nfo')
        
        try:
            if xbmcvfs.exists(category_path):
                self.log(f'Reading category.nfo from: {category_path}', xbmc.LOGDEBUG)
                
                file_obj = xbmcvfs.File(category_path, 'r')
                content = file_obj.read()
                file_obj.close()
                
                self.log(f'Category.nfo content length: {len(content)} bytes', xbmc.LOGDEBUG)
                
                # Parse XML
                root = ET.fromstring(content)
                for genre_elem in root.findall('.//genre'):
                    if genre_elem.text:
                        genre = genre_elem.text.strip()
                        genres.add(genre)
                        self.log(f'Found genre in category.nfo: {genre}', xbmc.LOGDEBUG)
                
                self.log(f'Successfully read {len(genres)} genres from {category_path}: {genres}', xbmc.LOGINFO)
            else:
                self.log(f'No category.nfo found at: {category_path}', xbmc.LOGDEBUG)
        except Exception as e:
            self.log(f'Error reading category.nfo from {path}: {e}', xbmc.LOGWARNING)
            self.log(f'Category.nfo read error traceback: {traceback.format_exc()}', xbmc.LOGWARNING)
        
        return genres
    
    def get_movie_nfo_mtime(self, path: str) -> float:
        """Get modification time of movie.nfo file"""
        nfo_path = os.path.join(path, 'movie.nfo')
        try:
            if xbmcvfs.exists(nfo_path):
                stat = xbmcvfs.Stat(nfo_path)
                mtime = stat.st_mtime()
                self.log(f'Movie.nfo mtime for {nfo_path}: {mtime} ({datetime.fromtimestamp(mtime)})', xbmc.LOGDEBUG)
                return mtime
            else:
                self.log(f'No movie.nfo found at: {nfo_path}', xbmc.LOGDEBUG)
        except Exception as e:
            self.log(f'Error getting movie.nfo mtime for {path}: {e}', xbmc.LOGDEBUG)
            self.log(f'Movie.nfo mtime error traceback: {traceback.format_exc()}', xbmc.LOGDEBUG)
        return 0
    
    def get_kodi_movie_date(self, path: str) -> float:
        """Get movie date from Kodi database via JSON-RPC"""
        try:
            self.log(f'Querying Kodi database for movie at path: {path}', xbmc.LOGDEBUG)
            
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
            
            self.log(f'JSON-RPC Request (GetMovies): {request}', xbmc.LOGDEBUG)
            response = xbmc.executeJSONRPC(request)
            self.log(f'JSON-RPC Response (GetMovies): {response}', xbmc.LOGDEBUG)
            
            result = json.loads(response)
            
            if 'result' in result and 'movies' in result['result'] and result['result']['movies']:
                movie = result['result']['movies'][0]
                # Parse dateadded to timestamp
                date_str = movie.get('dateadded', '')
                if date_str:
                    # Convert ISO format to timestamp
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    timestamp = dt.timestamp()
                    self.log(f'Movie in Kodi DB: {movie.get("file")} dated {date_str} (timestamp: {timestamp})', xbmc.LOGDEBUG)
                    return timestamp
                else:
                    self.log(f'Movie in DB but no dateadded: {movie.get("file")}', xbmc.LOGDEBUG)
            else:
                self.log(f'No movie found in Kodi DB for path: {path}', xbmc.LOGDEBUG)
        except Exception as e:
            self.log(f'Error getting movie date from Kodi DB for {path}: {e}', xbmc.LOGWARNING)
            self.log(f'Kodi DB query error traceback: {traceback.format_exc()}', xbmc.LOGWARNING)
        
        return 0
    
    def reimport_movie(self, path: str, genres: Set[str]) -> bool:
        """Re-import movie.nfo into Kodi database"""
        try:
            self.log(f'Starting re-import of movie from: {path}', xbmc.LOGINFO)
            self.log(f'Additional genres to add: {genres}', xbmc.LOGDEBUG)
            
            # Remove existing movie from library
            movie_id = self.get_movie_id_by_path(path)
            if movie_id is not None:
                self.log(f'Found existing movie with ID {movie_id}, removing...', xbmc.LOGDEBUG)
                
                request = json.dumps({
                    "jsonrpc": "2.0",
                    "method": "VideoLibrary.RemoveMovie",
                    "params": {
                        "movieid": movie_id
                    },
                    "id": 1
                })
                
                self.log(f'JSON-RPC Request (RemoveMovie): {request}', xbmc.LOGDEBUG)
                response = xbmc.executeJSONRPC(request)
                self.log(f'JSON-RPC Response (RemoveMovie): {response}', xbmc.LOGDEBUG)
            else:
                self.log(f'No existing movie found in DB for path: {path}', xbmc.LOGDEBUG)
            
            # Trigger scan of specific directory
            self.log(f'Triggering VideoLibrary.Scan for: {path}', xbmc.LOGDEBUG)
            
            request = json.dumps({
                "jsonrpc": "2.0",
                "method": "VideoLibrary.Scan",
                "params": {
                    "directory": path,
                    "showdialogs": False
                },
                "id": 1
            })
            
            self.log(f'JSON-RPC Request (Scan): {request}', xbmc.LOGDEBUG)
            response = xbmc.executeJSONRPC(request)
            self.log(f'JSON-RPC Response (Scan): {response}', xbmc.LOGDEBUG)
            
            result = json.loads(response)
            
            # If we have additional genres from category.nfo, add them
            if genres:
                self.log(f'Adding {len(genres)} additional genres from category.nfo: {genres}', xbmc.LOGDEBUG)
                self.add_genres_to_movie(path, genres)
            
            success = 'result' in result
            if success:
                self.log(f'Successfully re-imported movie from: {path}', xbmc.LOGINFO)
            else:
                self.log(f'Re-import may have failed for: {path}, result: {result}', xbmc.LOGWARNING)
            
            return success
        except Exception as e:
            self.log(f'Error re-importing movie from {path}: {e}', xbmc.LOGERROR)
            self.log(f'Movie re-import error traceback: {traceback.format_exc()}', xbmc.LOGERROR)
            return False
    
    def get_movie_id_by_path(self, path: str) -> Optional[int]:
        """Get movie ID from Kodi database by path"""
        try:
            self.log(f'Looking up movie ID for path: {path}', xbmc.LOGDEBUG)
            
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
            
            self.log(f'JSON-RPC Request (GetMovies for ID): {request}', xbmc.LOGDEBUG)
            response = xbmc.executeJSONRPC(request)
            self.log(f'JSON-RPC Response (GetMovies for ID): {response}', xbmc.LOGDEBUG)
            
            result = json.loads(response)
            
            if 'result' in result and 'movies' in result['result'] and result['result']['movies']:
                movie_id = result['result']['movies'][0].get('movieid')
                self.log(f'Found movie ID {movie_id} for path: {path}', xbmc.LOGDEBUG)
                return movie_id
            else:
                self.log(f'No movie ID found for path: {path}', xbmc.LOGDEBUG)
        except Exception as e:
            self.log(f'Error getting movie ID for {path}: {e}', xbmc.LOGWARNING)
            self.log(f'Movie ID lookup error traceback: {traceback.format_exc()}', xbmc.LOGWARNING)
        
        return None
    
    def add_genres_to_movie(self, path: str, genres: Set[str]):
        """Add genres from category.nfo to movie in Kodi database"""
        try:
            self.log(f'Adding genres {genres} to movie at path: {path}', xbmc.LOGDEBUG)
            
            movie_id = self.get_movie_id_by_path(path)
            if not movie_id:
                self.log(f'Cannot add genres: movie ID not found for path: {path}', xbmc.LOGWARNING)
                return
            
            self.log(f'Fetching current genres for movie ID {movie_id}', xbmc.LOGDEBUG)
            
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
            
            self.log(f'JSON-RPC Request (GetMovieDetails): {request}', xbmc.LOGDEBUG)
            response = xbmc.executeJSONRPC(request)
            self.log(f'JSON-RPC Response (GetMovieDetails): {response}', xbmc.LOGDEBUG)
            
            result = json.loads(response)
            
            current_genres = set()
            if 'result' in result and 'moviedetails' in result['result']:
                current_genres = set(result['result']['moviedetails'].get('genre', []))
                self.log(f'Current genres: {current_genres}', xbmc.LOGDEBUG)
            
            # Merge genres
            all_genres = current_genres | genres
            new_genres_added = all_genres - current_genres
            
            if new_genres_added:
                self.log(f'Adding new genres {new_genres_added} to existing {current_genres}', xbmc.LOGINFO)
                
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
                
                self.log(f'JSON-RPC Request (SetMovieDetails): {request}', xbmc.LOGDEBUG)
                response = xbmc.executeJSONRPC(request)
                self.log(f'JSON-RPC Response (SetMovieDetails): {response}', xbmc.LOGDEBUG)
                
                self.log(f'Successfully added genres to movie at {path}', xbmc.LOGINFO)
            else:
                self.log(f'No new genres to add for movie at {path}', xbmc.LOGDEBUG)
                
        except Exception as e:
            self.log(f'Error adding genres to movie at {path}: {e}', xbmc.LOGERROR)
            self.log(f'Genre addition error traceback: {traceback.format_exc()}', xbmc.LOGERROR)
    
    def scan_folder(self, path: str, parent_genres: Set[str] = None) -> int:
        """Scan a folder for movie.nfo and category.nfo files"""
        if not self.running or self.monitor.abortRequested():
            return 0
        
        # Wait if paused
        while self.paused and self.running:
            if self.monitor.waitForAbort(1):
                return 0
        
        # Log folder processing start
        start_time = time.time()
        self.log(f'=== Starting scan of folder: {path} ===', xbmc.LOGINFO)
        self.log(f'Parent genres: {parent_genres}', xbmc.LOGDEBUG)
        
        scanned_count = 0
        subdirs_count = 0
        has_movie_nfo = False
        has_category_nfo = False
        
        try:
            # Read category.nfo from current folder
            current_genres = self.read_category_nfo(path)
            has_category_nfo = len(current_genres) > 0
            
            # Merge with parent genres
            all_genres = (parent_genres or set()) | current_genres
            
            if current_genres:
                self.log(f'Merged genres for {path}: {all_genres}', xbmc.LOGDEBUG)
            
            # Check if movie.nfo exists
            nfo_mtime = self.get_movie_nfo_mtime(path)
            has_movie_nfo = nfo_mtime > 0
            
            if nfo_mtime > 0:
                self.log(f'Found movie.nfo in {path}', xbmc.LOGINFO)
                
                # Check if we need to re-import
                kodi_date = self.get_kodi_movie_date(path)
                
                self.log(f'Comparing dates - NFO: {nfo_mtime} ({datetime.fromtimestamp(nfo_mtime)}), '
                        f'Kodi DB: {kodi_date} ({datetime.fromtimestamp(kodi_date) if kodi_date > 0 else "not in DB"})',
                        xbmc.LOGDEBUG)
                
                if nfo_mtime > kodi_date:
                    self.log(f'NFO is newer than DB entry for {path}, re-importing...', xbmc.LOGINFO)
                    if self.reimport_movie(path, all_genres):
                        scanned_count += 1
                        self.log(f'Successfully re-imported movie from {path}', xbmc.LOGINFO)
                    else:
                        self.log(f'Failed to re-import movie from {path}', xbmc.LOGWARNING)
                elif all_genres and kodi_date > 0:
                    # Even if NFO is not newer, add genres from category.nfo
                    self.log(f'NFO not newer, but adding category genres to existing movie at {path}', xbmc.LOGDEBUG)
                    self.add_genres_to_movie(path, all_genres)
                elif kodi_date == 0:
                    self.log(f'Movie.nfo exists but movie not in Kodi DB: {path}', xbmc.LOGWARNING)
                else:
                    self.log(f'Movie.nfo up to date for {path}, skipping re-import', xbmc.LOGDEBUG)
            else:
                self.log(f'No movie.nfo found in {path}', xbmc.LOGDEBUG)
            
            # Scan subdirectories
            try:
                self.log(f'Listing subdirectories of {path}', xbmc.LOGDEBUG)
                dirs, files = xbmcvfs.listdir(path)
                
                subdirs_count = len(dirs)
                self.log(f'Found {subdirs_count} subdirectories and {len(files)} files in {path}', xbmc.LOGDEBUG)
                
                # Sort directories by modification time (newest first)
                dir_times = []
                for dir_name in dirs:
                    dir_path = os.path.join(path, dir_name)
                    mtime = self.get_folder_mtime(dir_path)
                    dir_times.append((mtime, dir_path))
                
                dir_times.sort(reverse=True)  # Newest first
                self.log(f'Sorted {len(dir_times)} directories by modification time', xbmc.LOGDEBUG)
                
                # Recursively scan subdirectories
                for idx, (mtime, dir_path) in enumerate(dir_times, 1):
                    if not self.running or self.monitor.abortRequested():
                        self.log(f'Scan interrupted for {path} at subdirectory {idx}/{len(dir_times)}', xbmc.LOGWARNING)
                        break
                    
                    self.log(f'Processing subdirectory {idx}/{len(dir_times)}: {dir_path}', xbmc.LOGDEBUG)
                    scanned_count += self.scan_folder(dir_path, all_genres)
                    
            except Exception as e:
                self.log(f'Error listing directory {path}: {e}', xbmc.LOGERROR)
                self.log(f'Directory listing error traceback: {traceback.format_exc()}', xbmc.LOGERROR)
        
        except Exception as e:
            self.log(f'Error scanning folder {path}: {e}', xbmc.LOGERROR)
            self.log(f'Folder scan error traceback: {traceback.format_exc()}', xbmc.LOGERROR)
        
        # Log folder processing end with statistics
        end_time = time.time()
        duration = end_time - start_time
        
        self.log(f'=== Completed scan of folder: {path} ===', xbmc.LOGINFO)
        self.log(f'Folder scan statistics:', xbmc.LOGINFO)
        self.log(f'  - Duration: {duration:.2f} seconds', xbmc.LOGINFO)
        self.log(f'  - Movies re-imported: {scanned_count}', xbmc.LOGINFO)
        self.log(f'  - Subdirectories processed: {subdirs_count}', xbmc.LOGINFO)
        self.log(f'  - Has movie.nfo: {has_movie_nfo}', xbmc.LOGINFO)
        self.log(f'  - Has category.nfo: {has_category_nfo}', xbmc.LOGINFO)
        if has_category_nfo:
            self.log(f'  - Category genres: {current_genres}', xbmc.LOGINFO)
        
        return scanned_count
    
    def scan_all_sources(self):
        """Scan all video sources"""
        scan_start_time = time.time()
        
        try:
            self.log('======================================', xbmc.LOGINFO)
            self.log('=== Starting full sources scan ===', xbmc.LOGINFO)
            self.log('======================================', xbmc.LOGINFO)
            
            sources = self.get_video_sources()
            if not sources:
                self.log('No video sources found to scan', xbmc.LOGWARNING)
                return
            
            self.log(f'Starting scan of {len(sources)} video sources', xbmc.LOGINFO)
            for idx, source in enumerate(sources, 1):
                self.log(f'  Source {idx}: {source["label"]} -> {source["path"]}', xbmc.LOGINFO)
            
            total_scanned = 0
            successful_sources = 0
            failed_sources = 0
            
            for idx, source in enumerate(sources, 1):
                if not self.running or self.monitor.abortRequested():
                    self.log('Scan interrupted by user or system', xbmc.LOGWARNING)
                    break
                
                path = source['path']
                label = source['label']
                
                source_start_time = time.time()
                self.log(f'>>> Starting scan of source {idx}/{len(sources)}: {label}', xbmc.LOGINFO)
                self.log(f'>>> Path: {path}', xbmc.LOGINFO)
                
                try:
                    scanned = self.scan_folder(path)
                    total_scanned += scanned
                    successful_sources += 1
                    
                    source_duration = time.time() - source_start_time
                    self.log(f'<<< Completed scan of source: {label}', xbmc.LOGINFO)
                    self.log(f'<<< Duration: {source_duration:.2f} seconds, Re-imported: {scanned} items', xbmc.LOGINFO)
                    
                except Exception as e:
                    failed_sources += 1
                    source_duration = time.time() - source_start_time
                    self.log(f'Error scanning source {label}: {e}', xbmc.LOGERROR)
                    self.log(f'Source scan error traceback: {traceback.format_exc()}', xbmc.LOGERROR)
                    self.log(f'<<< Failed scan of source: {label} after {source_duration:.2f} seconds', xbmc.LOGERROR)
            
            scan_duration = time.time() - scan_start_time
            
            self.log('======================================', xbmc.LOGINFO)
            self.log('=== Scan completed ===', xbmc.LOGINFO)
            self.log(f'Total scan duration: {scan_duration:.2f} seconds ({scan_duration/60:.2f} minutes)', xbmc.LOGINFO)
            self.log(f'Total sources scanned: {successful_sources}/{len(sources)}', xbmc.LOGINFO)
            self.log(f'Failed sources: {failed_sources}', xbmc.LOGINFO)
            self.log(f'Total movies re-imported: {total_scanned}', xbmc.LOGINFO)
            self.log('======================================', xbmc.LOGINFO)
            
        except Exception as e:
            scan_duration = time.time() - scan_start_time
            self.log(f'Critical error during scan: {e}', xbmc.LOGERROR)
            self.log(f'Scan critical error traceback: {traceback.format_exc()}', xbmc.LOGERROR)
            self.log(f'Scan aborted after {scan_duration:.2f} seconds', xbmc.LOGERROR)
    
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
        
        self.log('Scanner loop started', xbmc.LOGINFO)
        self.log(f'Scan interval: {self.scan_interval} minutes', xbmc.LOGINFO)
        
        while self.running and not self.monitor.abortRequested():
            try:
                current_time = time.time()
                scan_interval_seconds = self.scan_interval * 60
                time_since_last_scan = current_time - last_scan_time
                time_until_next_scan = scan_interval_seconds - time_since_last_scan
                
                # Log status periodically
                if time_until_next_scan > 0:
                    self.log(f'Next scan in {time_until_next_scan/60:.1f} minutes', xbmc.LOGDEBUG)
                
                # Check if it's time to scan
                if current_time - last_scan_time >= scan_interval_seconds:
                    if not self.paused:
                        self.log(f'Scan interval elapsed ({self.scan_interval} minutes), starting scan', xbmc.LOGINFO)
                        self.scan_all_sources()
                        last_scan_time = current_time
                        self.log(f'Next scan scheduled in {self.scan_interval} minutes', xbmc.LOGINFO)
                    else:
                        self.log('Scan interval elapsed but scanner is paused', xbmc.LOGINFO)
                
                # Wait a bit before checking again
                if self.monitor.waitForAbort(10):
                    self.log('Scanner loop: abort requested', xbmc.LOGINFO)
                    break
                    
            except Exception as e:
                self.log(f'Error in scanner loop: {e}', xbmc.LOGERROR)
                self.log(f'Scanner loop error traceback: {traceback.format_exc()}', xbmc.LOGERROR)
                if self.monitor.waitForAbort(30):
                    self.log('Scanner loop: abort requested after error', xbmc.LOGINFO)
                    break
        
        self.log('Scanner loop ended', xbmc.LOGINFO)
