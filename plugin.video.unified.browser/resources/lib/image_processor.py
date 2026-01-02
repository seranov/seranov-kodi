"""Image processor for creating composite images with overlay icons"""
import os
import hashlib
from io import BytesIO
from typing import Optional
import xbmc
import xbmcvfs

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    xbmc.log('[UnifiedBrowser] PIL/Pillow not available, image compositing disabled', xbmc.LOGWARNING)


class ImageProcessor:
    """Create composite images with overlay icons"""
    
    def __init__(self, cache_path: str):
        self.cache_path = cache_path
        self._ensure_cache_dir()
        self._create_overlay_icons()
    
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        cache_dir = xbmcvfs.translatePath(self.cache_path)
        if not xbmcvfs.exists(cache_dir):
            xbmcvfs.mkdirs(cache_dir)
    
    def _create_overlay_icons(self):
        """Create overlay icon images"""
        if not PIL_AVAILABLE:
            return
        
        # Create blue player icon (for single file)
        self.player_icon = self._create_player_icon()
        
        # Create yellow folder icon (for multiple files)
        self.folder_icon = self._create_folder_icon()
    
    def _create_player_icon(self, size: int = 64) -> Optional[Image.Image]:
        """Create a blue player icon"""
        try:
            # Create a blue circle with play triangle
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw blue circle
            draw.ellipse([0, 0, size-1, size-1], fill=(30, 144, 255, 230), outline=(20, 100, 200, 255))
            
            # Draw white play triangle
            triangle_size = size // 2
            offset = (size - triangle_size) // 2
            triangle = [
                (offset + triangle_size // 4, offset),
                (offset + triangle_size // 4, offset + triangle_size),
                (offset + triangle_size, offset + triangle_size // 2)
            ]
            draw.polygon(triangle, fill=(255, 255, 255, 255))
            
            return img
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error creating player icon: {e}', xbmc.LOGERROR)
            return None
    
    def _create_folder_icon(self, size: int = 64) -> Optional[Image.Image]:
        """Create a yellow folder icon"""
        try:
            # Create a yellow folder icon
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw folder shape
            # Folder tab
            tab_height = size // 4
            draw.rectangle([0, 0, size // 2, tab_height], fill=(255, 215, 0, 230), outline=(200, 170, 0, 255))
            
            # Folder body
            draw.rectangle([0, tab_height // 2, size-1, size-1], fill=(255, 215, 0, 230), outline=(200, 170, 0, 255))
            
            return img
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error creating folder icon: {e}', xbmc.LOGERROR)
            return None
    
    def create_composite_image(self, base_image_path: str, file_count: int) -> Optional[str]:
        """Create composite image with overlay icon
        
        Args:
            base_image_path: Path to folder.jpg
            file_count: Number of video files (1 = player icon, >1 = folder icon)
        
        Returns:
            Path to cached composite image, or None if creation failed
        """
        if not PIL_AVAILABLE:
            return base_image_path
        
        # Generate cache filename
        cache_key = f"{base_image_path}_{file_count}"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        cache_file = os.path.join(xbmcvfs.translatePath(self.cache_path), f"composite_{cache_hash}.png")
        
        # Return cached if exists
        if xbmcvfs.exists(cache_file):
            return cache_file
        
        try:
            # Load base image
            if not xbmcvfs.exists(base_image_path):
                return None
            
            # Read file using xbmcvfs
            file_obj = xbmcvfs.File(base_image_path, 'rb')
            image_data = file_obj.read()
            file_obj.close()
            
            # Load with PIL
            base_image = Image.open(BytesIO(image_data))
            
            # Convert to RGBA if needed
            if base_image.mode != 'RGBA':
                base_image = base_image.convert('RGBA')
            
            # Select overlay icon
            overlay = self.player_icon if file_count == 1 else self.folder_icon
            
            if overlay is None:
                return base_image_path
            
            # Calculate position (bottom-right corner)
            icon_size = min(base_image.width, base_image.height) // 4
            overlay = overlay.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            
            position = (
                base_image.width - icon_size - 10,
                base_image.height - icon_size - 10
            )
            
            # Composite images
            base_image.paste(overlay, position, overlay)
            
            # Save to cache
            base_image.save(cache_file, 'PNG')
            
            return cache_file
            
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error creating composite image: {e}', xbmc.LOGERROR)
            return base_image_path
    
    def clear_cache(self):
        """Clear image cache"""
        try:
            cache_dir = xbmcvfs.translatePath(self.cache_path)
            if xbmcvfs.exists(cache_dir):
                dirs, files = xbmcvfs.listdir(cache_dir)
                for filename in files:
                    file_path = os.path.join(cache_dir, filename)
                    xbmcvfs.delete(file_path)
                xbmc.log('[UnifiedBrowser] Image cache cleared', xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f'[UnifiedBrowser] Error clearing cache: {e}', xbmc.LOGERROR)
