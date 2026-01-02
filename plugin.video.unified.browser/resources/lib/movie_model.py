"""Movie data model and filtering logic"""
import os
from typing import List, Dict, Set, Optional
import xbmc
import xbmcvfs


class Movie:
    """Represents a movie (folder with one or more video files)"""
    
    def __init__(self, data: Dict):
        self.id = data.get('idMovie')
        self.title = data.get('title', 'Unknown')
        self.plot = data.get('plot', '')
        self.year = self._parse_year(data.get('year'))
        self.runtime = self._parse_runtime(data.get('runtime'))
        self.path = data.get('path', '')
        self.genres = data.get('genres', set())
        self.tags = data.get('tags', set())
        self.video_files = []
        self.folder_jpg = None
        
        # Find folder.jpg
        self._find_folder_jpg()
    
    def _parse_year(self, year_value) -> Optional[int]:
        """Parse year value to int"""
        if year_value is None:
            return None
        try:
            return int(year_value)
        except (ValueError, TypeError):
            return None
    
    def _parse_runtime(self, runtime_value) -> Optional[int]:
        """Parse runtime value to int"""
        if runtime_value is None:
            return None
        try:
            return int(runtime_value)
        except (ValueError, TypeError):
            return None
    
    def _find_folder_jpg(self):
        """Find folder.jpg in movie path"""
        if not self.path:
            return
        
        folder_jpg_path = os.path.join(self.path, 'folder.jpg')
        if xbmcvfs.exists(folder_jpg_path):
            self.folder_jpg = folder_jpg_path
    
    def get_folder_name(self) -> str:
        """Get folder name from path"""
        if self.path:
            return os.path.basename(os.path.normpath(self.path))
        return self.title
    
    def get_video_file_count(self) -> int:
        """Get number of video files"""
        return len(self.video_files)
    
    def has_multiple_files(self) -> bool:
        """Check if movie has multiple video files"""
        return len(self.video_files) > 1
    
    def get_display_title(self) -> str:
        """Get title for display"""
        return self.title or self.get_folder_name()
    
    def get_runtime_str(self) -> str:
        """Get formatted runtime string"""
        if self.runtime:
            hours = self.runtime // 60
            minutes = self.runtime % 60
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        return ""
    
    def matches_word_filter(self, include_words: str, exclude_words: str) -> bool:
        """Check if movie matches word filter
        
        Args:
            include_words: Space-separated words to include
            exclude_words: Space-separated words to exclude
        
        Returns:
            True if movie matches filter
        """
        search_text = f"{self.title} {self.plot}".lower()
        
        # Check include words (all must be present)
        if include_words:
            words = [w.strip().lower() for w in include_words.split() if w.strip()]
            for word in words:
                if word not in search_text:
                    return False
        
        # Check exclude words (none must be present)
        if exclude_words:
            words = [w.strip().lower() for w in exclude_words.split() if w.strip()]
            for word in words:
                if word in search_text:
                    return False
        
        return True


class MovieCollection:
    """Collection of movies with filtering capabilities"""
    
    def __init__(self):
        self.movies: List[Movie] = []
    
    def add_movie(self, movie: Movie):
        """Add movie to collection"""
        self.movies.append(movie)
    
    def filter_movies(self,
                      year_from: Optional[int] = None,
                      year_to: Optional[int] = None,
                      include_genres: Optional[Set[str]] = None,
                      exclude_genres: Optional[Set[str]] = None,
                      include_tags: Optional[Set[str]] = None,
                      exclude_tags: Optional[Set[str]] = None,
                      include_words: str = '',
                      exclude_words: str = '') -> List[Movie]:
        """Filter movies based on criteria
        
        Returns filtered list of movies
        """
        filtered = []
        
        for movie in self.movies:
            # Year filter
            if year_from is not None and movie.year is not None:
                if movie.year < year_from:
                    continue
            if year_to is not None and movie.year is not None:
                if movie.year > year_to:
                    continue
            
            # Genre filter
            if include_genres:
                if not movie.genres.intersection(include_genres):
                    continue
            if exclude_genres:
                if movie.genres.intersection(exclude_genres):
                    continue
            
            # Tag filter
            if include_tags:
                if not movie.tags.intersection(include_tags):
                    continue
            if exclude_tags:
                if movie.tags.intersection(exclude_tags):
                    continue
            
            # Word filter
            if not movie.matches_word_filter(include_words, exclude_words):
                continue
            
            filtered.append(movie)
        
        return filtered
    
    def get_all_genres(self) -> List[str]:
        """Get all unique genres from collection"""
        genres = set()
        for movie in self.movies:
            genres.update(movie.genres)
        return sorted(list(genres), key=lambda x: x.lower())
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags from collection"""
        tags = set()
        for movie in self.movies:
            tags.update(movie.tags)
        return sorted(list(tags), key=lambda x: x.lower())
    
    def count(self) -> int:
        """Get number of movies in collection"""
        return len(self.movies)
