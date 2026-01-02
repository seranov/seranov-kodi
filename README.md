# Kodi Add-ons Repository

This repository contains multiple Kodi add-ons and serves as a Kodi repository for easy installation.

## Repository Structure

```
├── plugin.video.random.recursive/  # Random Recursive Video Player plugin
├── context.screenshots/            # Popup Screenshots context menu addon
├── service.seranov.template1/      # Service plugin template 1
├── service.seranov.template2/      # Service plugin template 2
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

### Service Template 1
- **ID**: `service.seranov.template1`
- **Purpose**: A basic service template with configurable intervals
- **Features**:
  - Runs in the background
  - Configurable check interval
  - Debug mode support
  - Notification support

### Service Template 2
- **ID**: `service.seranov.template2`
- **Purpose**: An advanced service template with event monitoring
- **Features**:
  - Monitors playback events
  - Handles Kodi notifications
  - Reacts to settings changes
  - Configurable event handling

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

### Service Template Guidelines

**Template 1** is suitable for:
- Periodic tasks (checking for updates, monitoring conditions)
- Simple background services
- Services that run on a schedule

**Template 2** is suitable for:
- Event-driven services
- Monitoring playback or system events
- Services that need to react to Kodi notifications
- More complex interaction with Kodi

## Repository URL

When the repository is hosted on GitHub, add-ons can be installed by adding this repository URL to Kodi:

```
https://raw.githubusercontent.com/seranov/kodi-play-random/main/repo/
```

## License

MIT License - See LICENSE file for details

## Author

seranov (seranov@yandex.ru)
