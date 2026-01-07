# Kodi Add-ons Repository

> **[Русская версия / Russian version](doc/README.ru.md)**

This repository contains multiple Kodi add-ons and serves as a Kodi repository for easy installation.

## Documentation

- 📖 **[Installation Guide](doc/INSTALLATION.md)** - How to install the repository and add-ons
- 🚀 **[Quick Start Guide](doc/QUICKSTART.md)** - Get started quickly
- 🔧 **[Build & Publish Guide](doc/BUILD_AND_PUBLISH.md)** - Complete build and deployment instructions
- 🤝 **[Contributing Guide](doc/CONTRIBUTING.md)** - How to contribute and create new add-ons
- 📝 **[Release Notes](doc/RELEASE_NOTES.md)** - Latest changes and updates

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

📦 **Quick Start - Option 1 (URL Installation):**

⚠️ **Requires:** GitHub Pages must be activated first (see [KODI_URL_INSTALLATION.md](doc/KODI_URL_INSTALLATION.md))

1. In Kodi: **Settings** → **File manager** → **Add source**
2. Enter URL: `https://seranov.github.io/kodi-play-random/`
3. Name it (e.g., `Seranov Repo`)
4. **Add-ons** → **Install from zip file** → Select your source
5. Navigate to `repository.seranov/repository.seranov-1.0.0.zip`
6. Done! Now install add-ons from the repository

📦 **Quick Start - Option 2 (Manual ZIP):**

1. Download `repository.seranov-1.0.0.zip` from [Releases](https://github.com/seranov/kodi-play-random/releases/latest)
2. In Kodi: **Add-ons** → **Install from zip file**
3. Select the downloaded file
4. Done! Now install add-ons from the repository

📖 **Detailed Instructions:** See [Installation Guide](doc/INSTALLATION.md)  
🚀 **URL Setup Guide:** See [KODI_URL_INSTALLATION.md](doc/KODI_URL_INSTALLATION.md)

### Automatic Updates

✅ **Now Available!** The repository is published via GitHub Pages at:
```
https://seranov.github.io/kodi-play-random/
```

After installing the repository once, Kodi will automatically check for updates and notify you when new versions are available. No manual downloads needed!

## Development

### Automated Build & Deploy

The repository uses **GitHub Actions** for automated builds and deployment:

- ✅ Push to `main` branch triggers automatic build
- ✅ Generates ZIP archives for all add-ons
- ✅ Creates `addons.xml` and checksums
- ✅ Deploys to GitHub Pages automatically
- ✅ Users get automatic updates in Kodi

**Workflow:** `.github/workflows/publish-release.yml`

For complete build and deployment documentation, see [BUILD_AND_PUBLISH.md](doc/BUILD_AND_PUBLISH.md)

### Available Scripts

The `scripts/` directory contains tools for local development and testing:

1. **`generate_repo.py`** - Python script to build the repository locally
2. **`deploy-local.ps1`** - PowerShell script for local deployment to Kodi (Windows)
3. **`build-release.ps1`** - PowerShell script for testing release builds locally

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


## License

MIT License - See LICENSE file for details

## Author

seranov (seranov@yandex.ru)
