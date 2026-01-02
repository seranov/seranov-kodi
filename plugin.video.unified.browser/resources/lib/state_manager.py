"""State persistence manager for saving and restoring plugin state"""
import json
import os
from typing import Dict, Any, Optional, Set
import xbmc
import xbmcvfs


class StateManager:
    """Manage plugin state persistence"""
    
    def __init__(self, state_file: str = 'special://profile/addon_data/plugin.video.unified.browser/state.json'):
        self.state_file = xbmcvfs.translatePath(state_file)
        self._ensure_state_dir()
    
    def _ensure_state_dir(self):
        """Ensure state directory exists"""
        state_dir = os.path.dirname(self.state_file)
        if not xbmcvfs.exists(state_dir):
            xbmcvfs.mkdirs(state_dir)
    
    def save_state(self, state: Dict[str, Any]):
        """Save plugin state
        
        State includes:
        - current_view: int (0=filters, 1=list, 2=details)
        - current_position: int (position in movie list)
        - filters: dict with year_from, year_to, genres, tags, words
        - thumbnail_size: int
        """
        try:
            # Convert sets to lists for JSON serialization
            state_copy = state.copy()
            if 'filters' in state_copy:
                filters = state_copy['filters'].copy()
                for key in ['include_genres', 'exclude_genres', 'include_tags', 'exclude_tags']:
                    if key in filters and isinstance(filters[key], set):
                        filters[key] = list(filters[key])
                state_copy['filters'] = filters
            
            file_obj = xbmcvfs.File(self.state_file, 'w')
            file_obj.write(json.dumps(state_copy, indent=2))
            file_obj.close()
            
            xbmc.log('[UnifiedBrowser] State saved', xbmc.LOGDEBUG)
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error saving state: {e}', xbmc.LOGERROR)
    
    def load_state(self) -> Dict[str, Any]:
        """Load plugin state
        
        Returns default state if file doesn't exist or error occurs
        """
        default_state = {
            'current_view': 1,  # Start with movie list
            'current_position': 0,
            'filters': {
                'year_from': None,
                'year_to': None,
                'include_genres': set(),
                'exclude_genres': {'XXX'},  # Default: exclude XXX
                'include_tags': set(),
                'exclude_tags': set(),
                'include_words': '',
                'exclude_words': ''
            },
            'thumbnail_size': 200
        }
        
        try:
            if not xbmcvfs.exists(self.state_file):
                return default_state
            
            file_obj = xbmcvfs.File(self.state_file, 'r')
            content = file_obj.read()
            file_obj.close()
            
            state = json.loads(content)
            
            # Convert lists back to sets
            if 'filters' in state:
                filters = state['filters']
                for key in ['include_genres', 'exclude_genres', 'include_tags', 'exclude_tags']:
                    if key in filters and isinstance(filters[key], list):
                        filters[key] = set(filters[key])
            
            # Merge with defaults to handle missing keys
            merged_state = default_state.copy()
            merged_state.update(state)
            if 'filters' in state:
                merged_state['filters'] = default_state['filters'].copy()
                merged_state['filters'].update(state['filters'])
            
            xbmc.log('[UnifiedBrowser] State loaded', xbmc.LOGDEBUG)
            return merged_state
            
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error loading state: {e}', xbmc.LOGERROR)
            return default_state
    
    def clear_state(self):
        """Clear saved state"""
        try:
            if xbmcvfs.exists(self.state_file):
                xbmcvfs.delete(self.state_file)
                xbmc.log('[UnifiedBrowser] State cleared', xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error clearing state: {e}', xbmc.LOGERROR)
