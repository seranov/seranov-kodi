"""NFO file parser for additional metadata"""
import os
import xml.etree.ElementTree as ET
from typing import Dict, Optional, List
import xbmc
import xbmcvfs


class NFOParser:
    """Parse NFO files for movie metadata"""
    
    @staticmethod
    def parse_movie_nfo(folder_path: str) -> Optional[Dict]:
        """Parse movie.nfo file in folder
        
        Returns dictionary with:
        - title: movie title
        - plot: description
        - year: release year
        - genres: list of genres
        - tags: list of tags
        - runtime: runtime in minutes
        """
        nfo_path = os.path.join(folder_path, 'movie.nfo')
        
        try:
            if not xbmcvfs.exists(nfo_path):
                return None
            
            file_obj = xbmcvfs.File(nfo_path, 'r')
            content = file_obj.read()
            file_obj.close()
            
            # Parse XML
            # Note: Using ET.fromstring for compatibility with Kodi's bundled libraries.
            # Input is from local trusted NFO files, not external sources.
            root = ET.fromstring(content)
            
            metadata = {}
            
            # Extract title
            title_elem = root.find('title')
            if title_elem is not None and title_elem.text:
                metadata['title'] = title_elem.text.strip()
            
            # Extract plot
            plot_elem = root.find('plot')
            if plot_elem is not None and plot_elem.text:
                metadata['plot'] = plot_elem.text.strip()
            
            # Extract year
            year_elem = root.find('year')
            if year_elem is not None and year_elem.text:
                try:
                    metadata['year'] = int(year_elem.text.strip())
                except ValueError:
                    pass
            
            # Extract genres
            genres = []
            for genre_elem in root.findall('genre'):
                if genre_elem.text:
                    genres.append(genre_elem.text.strip())
            if genres:
                metadata['genres'] = genres
            
            # Extract tags
            tags = []
            for tag_elem in root.findall('tag'):
                if tag_elem.text:
                    tags.append(tag_elem.text.strip())
            if tags:
                metadata['tags'] = tags
            
            # Extract runtime
            runtime_elem = root.find('runtime')
            if runtime_elem is not None and runtime_elem.text:
                try:
                    metadata['runtime'] = int(runtime_elem.text.strip())
                except ValueError:
                    pass
            
            return metadata if metadata else None
            
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error parsing NFO {nfo_path}: {e}', xbmc.LOGDEBUG)
            return None
    
    @staticmethod
    def parse_category_nfo(folder_path: str) -> List[str]:
        """Parse category.nfo for folder-level genres
        
        Returns list of genres
        """
        nfo_path = os.path.join(folder_path, 'category.nfo')
        
        try:
            if not xbmcvfs.exists(nfo_path):
                return []
            
            file_obj = xbmcvfs.File(nfo_path, 'r')
            content = file_obj.read()
            file_obj.close()
            
            # Parse XML
            # Note: Using ET.fromstring for compatibility with Kodi's bundled libraries.
            # Input is from local trusted NFO files, not external sources.
            root = ET.fromstring(content)
            
            genres = []
            for genre_elem in root.findall('.//genre'):
                if genre_elem.text:
                    genres.append(genre_elem.text.strip())
            
            return genres
            
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error parsing category NFO {nfo_path}: {e}', xbmc.LOGDEBUG)
            return []
