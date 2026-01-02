"""Main plugin entry point for Unified Video Browser"""
import sys
import os
from urllib.parse import parse_qs
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

# Import library modules
from resources.lib.kodi_database import KodiDatabase
from resources.lib.nfo_parser import NFOParser
from resources.lib.movie_model import Movie, MovieCollection
from resources.lib.image_processor import ImageProcessor
from resources.lib.state_manager import StateManager

# Get addon information
addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1]) if len(sys.argv) > 1 else -1
addon_url = sys.argv[0] if len(sys.argv) > 0 else ''


def log(msg, level=xbmc.LOGINFO):
    """Log message"""
    xbmc.log(f'[UnifiedBrowser] {msg}', level)


class UnifiedBrowserPlugin:
    """Main plugin class"""
    
    def __init__(self):
        self.addon = addon
        self.handle = addon_handle
        self.url = addon_url
        
        # Initialize components
        self.db = KodiDatabase()
        self.nfo_parser = NFOParser()
        self.state_manager = StateManager()
        
        # Get settings
        cache_path = self.addon.getSetting('cache_path')
        self.image_processor = ImageProcessor(cache_path)
        
        # Load state
        self.state = self.state_manager.load_state()
        
        # Movie collection
        self.movies = MovieCollection()
        self.filtered_movies = []
    
    def load_movies(self):
        """Load movies from database"""
        try:
            log('Loading movies from database...')
            
            # Get filters from state
            filters = self.state.get('filters', {})
            
            # Query database
            movie_data_list = self.db.get_movies(
                year_from=filters.get('year_from'),
                year_to=filters.get('year_to'),
                include_genres=filters.get('include_genres'),
                exclude_genres=filters.get('exclude_genres'),
                include_tags=filters.get('include_tags'),
                exclude_tags=filters.get('exclude_tags')
            )
            
            # Create movie objects
            self.movies = MovieCollection()
            for movie_data in movie_data_list:
                movie = Movie(movie_data)
                
                # Get video files for this movie path
                if movie.path:
                    video_files = self.db.get_video_files_for_path(movie.path)
                    movie.video_files = video_files
                
                self.movies.add_movie(movie)
            
            # Apply word filters
            include_words = filters.get('include_words', '')
            exclude_words = filters.get('exclude_words', '')
            self.filtered_movies = self.movies.filter_movies(
                include_words=include_words,
                exclude_words=exclude_words
            )
            
            log(f'Loaded {len(self.filtered_movies)} movies')
            
        except Exception as e:
            log(f'Error loading movies: {e}', xbmc.LOGERROR)
            self.filtered_movies = []
    
    def show_filters_view(self):
        """Show filters view (View 1)"""
        log('Showing filters view')
        
        # Create a simple list for navigation
        xbmcplugin.setContent(self.handle, 'files')
        
        # Year range option
        list_item = xbmcgui.ListItem(label='Year Range')
        url = f'{self.url}?action=edit_year_range'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        # Genres option
        list_item = xbmcgui.ListItem(label='Edit Genres Filter')
        url = f'{self.url}?action=edit_genres'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        # Tags option
        list_item = xbmcgui.ListItem(label='Edit Tags Filter')
        url = f'{self.url}?action=edit_tags'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        # Word filter option
        list_item = xbmcgui.ListItem(label='Edit Word Filter')
        url = f'{self.url}?action=edit_words'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        # Reset filters option
        list_item = xbmcgui.ListItem(label='Reset All Filters')
        url = f'{self.url}?action=reset_filters'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        # Go to movie list
        list_item = xbmcgui.ListItem(label='→ View Movie List')
        url = f'{self.url}?action=show_list'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        xbmcplugin.endOfDirectory(self.handle)
    
    def show_movie_list_view(self):
        """Show movie list view (View 2)"""
        log('Showing movie list view')
        
        # Load movies if not loaded
        if not self.filtered_movies:
            self.load_movies()
        
        xbmcplugin.setContent(self.handle, 'movies')
        
        # Add navigation to filters
        list_item = xbmcgui.ListItem(label='← Edit Filters')
        url = f'{self.url}?action=show_filters'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        # Show movie count
        count_label = f"Movies: {len(self.filtered_movies)}"
        list_item = xbmcgui.ListItem(label=count_label)
        xbmcplugin.addDirectoryItem(self.handle, '', list_item, isFolder=False)
        
        # Add movies
        for idx, movie in enumerate(self.filtered_movies):
            list_item = xbmcgui.ListItem(label=movie.get_display_title())
            
            # Set info
            info = {
                'title': movie.get_display_title(),
                'plot': movie.plot,
                'year': movie.year,
                'duration': movie.runtime * 60 if movie.runtime else 0
            }
            list_item.setInfo('video', info)
            
            # Set artwork
            if movie.folder_jpg:
                # Create composite image if we have overlay
                composite_img = self.image_processor.create_composite_image(
                    movie.folder_jpg,
                    movie.get_video_file_count()
                )
                if composite_img:
                    list_item.setArt({'thumb': composite_img, 'poster': composite_img})
            
            # Determine action based on file count
            if movie.get_video_file_count() == 1 and movie.video_files:
                # Single file - play directly
                video_file = os.path.join(movie.path, movie.video_files[0])
                url = video_file
                is_folder = False
                list_item.setProperty('IsPlayable', 'true')
            elif movie.get_video_file_count() > 1:
                # Multiple files - show file list
                url = f'{self.url}?action=show_files&movie_id={idx}'
                is_folder = True
            else:
                # No files - just show details
                url = f'{self.url}?action=show_details&movie_id={idx}'
                is_folder = False
            
            xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=is_folder)
        
        # Add navigation to details
        list_item = xbmcgui.ListItem(label='→ View Details')
        url = f'{self.url}?action=show_details'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        xbmcplugin.endOfDirectory(self.handle)
    
    def show_files_for_movie(self, movie_id: int):
        """Show list of video files for a movie"""
        log(f'Showing files for movie {movie_id}')
        
        if movie_id >= len(self.filtered_movies):
            return
        
        movie = self.filtered_movies[movie_id]
        
        xbmcplugin.setContent(self.handle, 'files')
        
        # Add back navigation
        list_item = xbmcgui.ListItem(label='← Back to Movie List')
        url = f'{self.url}?action=show_list'
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, isFolder=False)
        
        # Add video files
        for video_file in movie.video_files:
            list_item = xbmcgui.ListItem(label=video_file)
            list_item.setProperty('IsPlayable', 'true')
            
            video_path = os.path.join(movie.path, video_file)
            xbmcplugin.addDirectoryItem(self.handle, video_path, list_item, isFolder=False)
        
        xbmcplugin.endOfDirectory(self.handle)
    
    def show_details_view(self, movie_id: int = None):
        """Show details view (View 3)"""
        log('Showing details view')
        
        if movie_id is not None and movie_id < len(self.filtered_movies):
            movie = self.filtered_movies[movie_id]
            # For now, just show a simple view
            # Full implementation would show thumbnails from subfolders
            dialog = xbmcgui.Dialog()
            dialog.textviewer(movie.get_display_title(), movie.plot or 'No description available')
        
        # For now, redirect back to list
        self.show_movie_list_view()
    
    def edit_year_range(self):
        """Edit year range filter"""
        filters = self.state['filters']
        
        dialog = xbmcgui.Dialog()
        
        # Get year from
        year_from = dialog.numeric(0, 'Year from (leave 0 for no limit)', 
                                    str(filters.get('year_from') or 0))
        if year_from:
            year_from = int(year_from)
            filters['year_from'] = year_from if year_from > 0 else None
        
        # Get year to
        year_to = dialog.numeric(0, 'Year to (leave 0 for no limit)', 
                                 str(filters.get('year_to') or 0))
        if year_to:
            year_to = int(year_to)
            filters['year_to'] = year_to if year_to > 0 else None
        
        self.state_manager.save_state(self.state)
        
        # Reload movies
        self.load_movies()
        
        # Show list
        self.show_movie_list_view()
    
    def reset_filters(self):
        """Reset all filters to default"""
        self.state['filters'] = {
            'year_from': None,
            'year_to': None,
            'include_genres': set(),
            'exclude_genres': {'XXX'},
            'include_tags': set(),
            'exclude_tags': set(),
            'include_words': '',
            'exclude_words': ''
        }
        self.state_manager.save_state(self.state)
        
        # Reload movies
        self.load_movies()
        
        xbmcgui.Dialog().notification(
            self.addon.getAddonInfo('name'),
            self.addon.getLocalizedString(32403),
            xbmcgui.NOTIFICATION_INFO
        )
    
    def run(self, params: dict):
        """Main entry point"""
        action = params.get('action', [''])[0]
        
        log(f'Action: {action}')
        
        if action == 'show_filters':
            self.show_filters_view()
        elif action == 'show_list':
            self.show_movie_list_view()
        elif action == 'show_files':
            movie_id = int(params.get('movie_id', ['0'])[0])
            self.show_files_for_movie(movie_id)
        elif action == 'show_details':
            movie_id_str = params.get('movie_id', [''])[0]
            movie_id = int(movie_id_str) if movie_id_str else None
            self.show_details_view(movie_id)
        elif action == 'edit_year_range':
            self.edit_year_range()
        elif action == 'reset_filters':
            self.reset_filters()
        else:
            # Default: show movie list
            self.show_movie_list_view()


if __name__ == '__main__':
    try:
        # Parse parameters
        params = parse_qs(sys.argv[2][1:]) if len(sys.argv) > 2 else {}
        
        # Create and run plugin
        plugin = UnifiedBrowserPlugin()
        plugin.run(params)
        
    except Exception as e:
        log(f'Plugin error: {e}', xbmc.LOGERROR)
        import traceback
        log(traceback.format_exc(), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            addon.getAddonInfo('name'),
            addon.getLocalizedString(32404).format(str(e)),
            xbmcgui.NOTIFICATION_ERROR
        )
