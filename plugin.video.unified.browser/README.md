# Unified Video Browser Plugin

## Description

A Kodi plugin that shows video files, movies and series in a unified list without separation by content type. Browse all your video content in a single interface with powerful filtering capabilities.

## Features

- **Unified View**: All videos, movies and TV series in one place
- **Smart Movie Detection**: Treats folders with video files as "movies"
  - Single video file: plays directly with blue player icon overlay
  - Multiple video files: shows file list with yellow folder icon overlay
- **Three View System**:
  1. **Filters View**: Configure year range, genres, tags, and keyword filters
  2. **Movie List View**: Browse filtered movies with poster art and details
  3. **Details View**: Detailed information with thumbnail gallery
- **Persistent State**: Remembers your position, filters, and view settings
- **Genre & Tag Filtering**: 3-state checkboxes (include/ignore/exclude)
- **Keyword Search**: Include or exclude words from title and description
- **Composite Images**: Automatic overlay icons on folder.jpg images
- **Default Filter**: Automatically excludes "XXX" genre/tag

## Requirements

- Kodi Omega 21.x or later
- Python 3.0+ (included with Kodi)
- PIL/Pillow for image processing (script.module.pil addon)
- Configured video sources in Kodi
- Video library with metadata (from NFO files or scrapers)

## Installation

1. Install via Seranov's Kodi Repository, or
2. Download the zip file and install via "Install from zip file" in Kodi

## Usage

1. Open the plugin from Video Add-ons
2. The main view shows your movie list
3. Use left/right arrows to switch between views:
   - Left: Go to Filters view
   - Right: Go to Details view
4. In Filters view:
   - Set year range (from/to)
   - Configure genre filters (include/exclude)
   - Configure tag filters (include/exclude)
   - Set keyword filters (include/exclude words)
5. Select a movie:
   - Single file: plays immediately
   - Multiple files: shows file selection
6. Your position and filters are saved automatically

## Data Sources

The plugin reads from:
- Kodi's MyVideos database (movies, genres, tags)
- NFO files in video folders (movie.nfo, category.nfo)
- Kodi's virtual file system (video sources)

## Settings

- **Cache Path**: Location for composite image cache
- **Default Thumbnail Size**: Initial size for thumbnails in Details view
- **Default View**: Which view to open by default (Filters/List/Details)
- **Debug Logging**: Enable detailed logging for troubleshooting

## Technical Details

### File Structure
```
plugin.video.unified.browser/
├── addon.xml                    # Plugin metadata
├── main.py                      # Main plugin script
├── icon.png                     # Plugin icon
├── README.md                    # This file
└── resources/
    ├── settings.xml             # Settings definition
    ├── language/
    │   └── resource.language.en_gb/
    │       └── strings.xml      # English strings
    └── lib/
        ├── kodi_database.py     # Database connector
        ├── nfo_parser.py        # NFO file parser
        ├── movie_model.py       # Movie data model
        ├── image_processor.py   # Image compositing
        └── state_manager.py     # State persistence
```

### Database Schema

The plugin reads from Kodi's MyVideos database tables:
- `movie`: Movie metadata
- `files`: Video file information
- `path`: File paths
- `tag`: Tag information
- `tag_link`: Tag associations

### State Persistence

Plugin state is saved to:
```
special://profile/addon_data/plugin.video.unified.browser/state.json
```

State includes:
- Current view (0=filters, 1=list, 2=details)
- Current position in movie list
- Active filters (years, genres, tags, words)
- Thumbnail size preference

### Image Cache

Composite images (folder.jpg + overlay icon) are cached in:
```
special://temp/unified_browser_cache/
```

Cache can be cleared from settings or by deleting the folder.

## Troubleshooting

### No movies shown
- Check that video sources are configured in Kodi
- Ensure video library has been scanned
- Check that filters aren't excluding all content
- Try resetting filters from Filters view

### Missing thumbnails
- Ensure folder.jpg exists in movie folders
- Check cache path is writable
- Verify PIL/Pillow addon is installed

### Performance issues
- Reduce number of movies in library
- Clear image cache periodically
- Disable debug logging

## Development

### Building
```bash
python3 scripts/generate_repo.py
```

### Testing
Deploy to local Kodi installation for testing:
```powershell
.\scripts\deploy-local.ps1 -AddonsToDeploy @('plugin.video.unified.browser')
```

## License

MIT License - See LICENSE file for details

## Author

seranov (seranov@yandex.ru)

## Support

Report issues at: https://github.com/seranov/kodi-play-random
