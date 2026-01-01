# Kodi Add-ons Repository

This repository contains multiple Kodi add-ons and serves as a Kodi repository for easy installation.

## Repository Structure

```
├── repository.seranov/          # Repository addon
├── service.seranov.template1/   # Service plugin template 1
├── service.seranov.template2/   # Service plugin template 2
├── addon.xml                    # Random Recursive Video Player plugin (root level)
├── main.py                      # Main plugin file
├── resources/                   # Plugin resources
├── repo/                        # Generated repository files (addons.xml, zips)
└── scripts/                     # Build scripts
```

**Note**: The existing Random Recursive Video Player plugin (`plugin.video.random.recursive`) files are located at the repository root level. New plugins should be created in their own directories (see templates).

## Available Add-ons

### Repository Add-on
- **ID**: `repository.seranov`
- **Purpose**: Install this to get automatic updates for all add-ons in this repository

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

### Building the Repository

To generate the repository files (addons.xml, MD5 checksums, and zip files):

```bash
python3 scripts/generate_repo.py
```

This will:
1. Create zip files for all add-ons in the `repo` directory
2. Generate `addons.xml` with metadata for all add-ons
3. Generate `addons.xml.md5` checksum file

### Adding New Add-ons

1. Create a new directory with the add-on ID as the name (e.g., `service.seranov.newaddon`)
2. Add the required files:
   - `addon.xml` - Add-on metadata
   - `service.py` or `main.py` - Main script
   - `icon.png` - Add-on icon (256x256 recommended)
   - `resources/settings.xml` - Settings configuration
   - `resources/language/resource.language.en_gb/strings.po` - Localization strings
3. Run the build script to regenerate the repository

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
    │       └── strings.po       # English strings
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
