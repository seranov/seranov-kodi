# Kodi Add-ons Repository

This repository contains multiple Kodi add-ons and serves as a Kodi repository for easy installation.

## Repository Structure

```
├── plugin.video.random.recursive/  # Random Recursive Video Player plugin
├── plugin.video.unified.browser/   # Unified Video Browser plugin
├── context.screenshots/            # Popup Screenshots context menu addon
├── service.seranov.nfoscanner/     # NFO Scanner Service
├── repository.seranov/             # Repository addon
├── repo/                           # Generated repository files (addons.xml, zips)
└── scripts/                        # Build scripts
```

## Available Add-ons

### Repository Add-on
- **ID**: `repository.seranov`
- **Purpose**: Install this to get automatic updates for all add-ons in this repository

### Random Recursive Video Player
- **ID**: `plugin.video.random.recursive`
- **Purpose**: Play videos recursively in random order from a directory
- **Features**:
  - Scans directories recursively for video files
  - Plays videos in random order
  - Context menu integration
  - Automatic playlist management

### Popup Screenshots
- **ID**: `context.screenshots`
- **Purpose**: Display local screenshots and images in a slideshow
- **Features**:
  - Context menu integration for media items
  - Slideshow of local images
  - Support for file_id.diz text files
  - Lightweight and easy to use

### Unified Video Browser
- **ID**: `plugin.video.unified.browser`
- **Purpose**: Browse all video content in a unified list without separation by content type
- **Features**:
  - Shows videos, movies and series in a single interface
  - Three-view system: Filters, Movie List, and Details
  - Advanced filtering by year range, genres, tags, and keywords
  - Composite images with overlay icons (blue player for single files, yellow folder for multiple)
  - Persistent state (remembers position, filters, and view)
  - Smart movie detection (folders with video files)
  - Default XXX genre/tag exclusion
  - Image caching for performance
  - Direct playback for single files, file list for multiple files

### NFO Scanner Service
- **ID**: `service.seranov.nfoscanner`
- **Purpose**: Background service that scans video folders for movie.nfo and category.nfo files
- **Features**:
  - Automatic scanning of video sources for metadata changes
  - Re-imports movies when movie.nfo is newer than Kodi database
  - Processes category.nfo files for genre management
  - Pauses during video playback to avoid interference
  - Configurable scan intervals and thread count
  - Manual scan controls
  - Priority scanning based on user folder navigation
  - Supports both local and network sources

## Installation

### Method 1: Install Repository (Recommended)

1. Download the repository zip file: `repository.seranov-1.0.0.zip` from the `repo` folder
2. In Kodi, go to **Add-ons** → **Install from zip file**
3. Browse to the downloaded zip file and install it
4. Go to **Install from repository** → **Seranov's Kodi Repository**
5. Install any add-ons you want from the repository

### Method 2: Install Individual Add-on

1. Download the specific add-on zip file from the `repo` folder
2. In Kodi, go to **Add-ons** → **Install from zip file**
3. Browse to the downloaded zip file and install it

## Development

### Available Scripts

The `scripts/` directory contains tools for development and publishing:

1. **`generate_repo.py`** - Python script to build the repository
2. **`deploy-local.ps1`** - PowerShell script for local deployment to Kodi (Windows)
3. **`build-release.ps1`** - PowerShell script for building releases and publishing to GitHub

For detailed documentation, see [scripts/README.md](scripts/README.md)

### Building the Repository

To generate the repository files (addons.xml, MD5 checksums, and zip files):

```bash
python3 scripts/generate_repo.py
```

Or use the PowerShell script for a complete release build:

```powershell
.\scripts\build-release.ps1
```

This will:
1. Create zip files for all add-ons in the `repo` directory
2. Generate `addons.xml` with metadata for all add-ons
3. Generate `addons.xml.md5` checksum file
4. Provide instructions for publishing to GitHub

### Local Deployment for Testing

For quick deployment to your local Kodi installation (Windows):

```powershell
# Deploy all addons
.\scripts\deploy-local.ps1

# Deploy specific addon
.\scripts\deploy-local.ps1 -AddonsToDeploy @('plugin.video.random.recursive')
```

### Adding New Add-ons

1. Create a new directory with the add-on ID as the name (e.g., `plugin.video.newaddon`, `service.seranov.newaddon`, `context.newaddon`)
2. Add the required files:
   - `addon.xml` - Add-on metadata
   - `service.py`, `main.py`, or `addon.py` - Main script
   - `icon.png` - Add-on icon (256x256 recommended)
   - `resources/settings.xml` - Settings configuration (optional)
   - `resources/language/resource.language.en_gb/strings.po` - Localization strings
3. Run the build script to regenerate the repository

The build script automatically detects all directories starting with `plugin.`, `service.`, `context.`, or `repository.`

### Service Plugin Template Structure

Each service plugin should have:

### Service Plugin Template Structure

Each service plugin should have:

```
service.addon.name/
├── addon.xml                    # Add-on metadata
├── service.py                   # Main service script
├── icon.png                     # Add-on icon
├── fanart.jpg                   # Optional fanart
└── resources/
    ├── settings.xml             # Add-on settings
    ├── language/
    │   └── resource.language.en_gb/
    │       └── strings.xml       # English strings
    └── lib/                     # Optional library modules
```

## Repository URL

When the repository is hosted on GitHub, add-ons can be installed by adding this repository URL to Kodi:

```
https://raw.githubusercontent.com/seranov/kodi-play-random/main/repo/
```

## License

MIT License - See LICENSE file for details

## Author

seranov (seranov@yandex.ru)
