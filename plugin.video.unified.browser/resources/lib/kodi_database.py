"""Database connector for Kodi MyVideos database"""
import os
import sqlite3
from typing import List, Dict, Optional, Set
import xbmc
import xbmcvfs


class KodiDatabase:
    """Interface to Kodi's MyVideos database"""
    
    def __init__(self):
        self.db_path = self._find_database()
        self.connection = None
        
    def _find_database(self) -> str:
        """Find the Kodi video database"""
        # Kodi stores databases in special://database/
        db_folder = xbmcvfs.translatePath('special://database/')
        
        # Look for MyVideos database (usually MyVideos116.db for Kodi 20+)
        # We need to find the highest numbered version
        max_version = 0
        db_file = None
        
        try:
            dirs, files = xbmcvfs.listdir(db_folder)
            for filename in files:
                if filename.startswith('MyVideos') and filename.endswith('.db'):
                    # Extract version number
                    try:
                        version = int(filename.replace('MyVideos', '').replace('.db', ''))
                        if version > max_version:
                            max_version = version
                            db_file = os.path.join(db_folder, filename)
                    except ValueError:
                        pass
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error finding database: {e}', xbmc.LOGERROR)
        
        if not db_file:
            # Fallback to common name
            db_file = os.path.join(db_folder, 'MyVideos116.db')
        
        xbmc.log(f'[UnifiedBrowser] Using database: {db_file}', xbmc.LOGINFO)
        return db_file
    
    def connect(self):
        """Open database connection"""
        try:
            # Open in read-only mode to prevent accidental writes
            db_uri = f'file:{self.db_path}?mode=ro'
            self.connection = sqlite3.connect(db_uri, uri=True)
            self.connection.row_factory = sqlite3.Row
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error connecting to database: {e}', xbmc.LOGERROR)
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def get_movies(self, 
                   year_from: Optional[int] = None,
                   year_to: Optional[int] = None,
                   include_genres: Optional[Set[str]] = None,
                   exclude_genres: Optional[Set[str]] = None,
                   include_tags: Optional[Set[str]] = None,
                   exclude_tags: Optional[Set[str]] = None) -> List[Dict]:
        """Get movies from database with optional filters
        
        Returns list of dictionaries with movie information:
        - idMovie: database ID
        - c00: title
        - c01: plot (description)
        - c07: year
        - c11: runtime (minutes)
        - c14: genre (comma-separated)
        - c19: folder path
        """
        if not self.connection:
            self.connect()
        
        query = """
            SELECT 
                m.idMovie,
                m.c00 as title,
                m.c01 as plot,
                m.c07 as year,
                m.c11 as runtime,
                m.c14 as genre_str,
                p.strPath as path
            FROM movie m
            LEFT JOIN files f ON m.idFile = f.idFile
            LEFT JOIN path p ON f.idPath = p.idPath
            WHERE 1=1
        """
        params = []
        
        # Year filters
        if year_from is not None:
            query += " AND CAST(m.c07 AS INTEGER) >= ?"
            params.append(year_from)
        if year_to is not None:
            query += " AND CAST(m.c07 AS INTEGER) <= ?"
            params.append(year_to)
        
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        
        movies = []
        for row in cursor.fetchall():
            movie = dict(row)
            
            # Parse genres
            genre_str = movie.get('genre_str', '') or ''
            movie_genres = set(g.strip() for g in genre_str.split('/') if g.strip())
            movie['genres'] = movie_genres
            
            # Get tags for this movie
            movie_tags = self._get_movie_tags(movie['idMovie'])
            movie['tags'] = movie_tags
            
            # Apply genre filters
            if include_genres:
                if not movie_genres.intersection(include_genres):
                    continue
            if exclude_genres:
                if movie_genres.intersection(exclude_genres):
                    continue
            
            # Apply tag filters
            if include_tags:
                if not movie_tags.intersection(include_tags):
                    continue
            if exclude_tags:
                if movie_tags.intersection(exclude_tags):
                    continue
            
            movies.append(movie)
        
        return movies
    
    def _get_movie_tags(self, movie_id: int) -> Set[str]:
        """Get tags for a specific movie"""
        if not self.connection:
            return set()
        
        query = """
            SELECT t.name
            FROM tag t
            JOIN tag_link tl ON t.tag_id = tl.tag_id
            WHERE tl.media_id = ? AND tl.media_type = 'movie'
        """
        
        cursor = self.connection.cursor()
        cursor.execute(query, (movie_id,))
        
        tags = set()
        for row in cursor.fetchall():
            tags.add(row[0])
        
        return tags
    
    def get_all_genres(self) -> List[str]:
        """Get all unique genres from database"""
        if not self.connection:
            self.connect()
        
        query = "SELECT DISTINCT c14 FROM movie WHERE c14 IS NOT NULL AND c14 != ''"
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        genres = set()
        for row in cursor.fetchall():
            genre_str = row[0]
            for genre in genre_str.split('/'):
                genre = genre.strip()
                if genre:
                    genres.add(genre)
        
        return sorted(list(genres), key=lambda x: x.lower())
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags from database"""
        if not self.connection:
            self.connect()
        
        query = """
            SELECT DISTINCT t.name
            FROM tag t
            JOIN tag_link tl ON t.tag_id = tl.tag_id
            WHERE tl.media_type = 'movie'
            ORDER BY t.name COLLATE NOCASE
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        return [row[0] for row in cursor.fetchall()]
    
    def get_video_files_for_path(self, path: str) -> List[str]:
        """Get video files in a specific path"""
        if not self.connection:
            self.connect()
        
        query = """
            SELECT f.strFilename
            FROM files f
            JOIN path p ON f.idPath = p.idPath
            WHERE p.strPath = ?
            ORDER BY f.strFilename
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (path,))
        
        return [row[0] for row in cursor.fetchall()]
