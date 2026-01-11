# GitHub Pages Deployment - User Guide

## Overview

This document describes how the GitHub Pages deployment works and what users will see when visiting your Kodi repository.

## Deployment Structure

When the GitHub Actions workflow runs, it creates the following structure in the `docs/` directory:

```
docs/
├── .nojekyll                          # Disables Jekyll processing
├── readme.html                        # Main landing page with addon cards
├── addons.xml                         # Repository metadata for Kodi
├── addons.xml.md5                     # Checksum for validation
│
├── doc/                               # Documentation (converted from Markdown)
│   ├── README.html
│   ├── QUICKSTART.html
│   ├── INSTALLATION.html
│   ├── CONTRIBUTING.html
│   └── ... (all .md files from /doc directory)
│
└── [addon-directories]/               # Each addon gets its own directory
    ├── context.screenshots/
    │   ├── context.screenshots-1.0.5.zip
    │   ├── icon.png
    │   └── fanart.jpg
    │
    ├── plugin.video.unified.browser/
    │   ├── plugin.video.unified.browser-1.0.0.zip
    │   └── icon.png
    │
    └── ... (other addons)
```

## Main Landing Page (readme.html)

The `readme.html` file serves as the main landing page for your repository. It includes:

### Features
- **Modern responsive design** with gradient background
- **Addon cards** for each available add-on with:
  - Add-on name and version
  - English summary and description
  - Download ZIP button
  - View files link
  
- **Installation instructions** with two methods:
  1. Repository method (recommended)
  2. Direct ZIP installation

- **Documentation links** to all converted HTML documents
- **Repository metadata links** (addons.xml, addons.xml.md5)

### CSS Styling
The page includes embedded CSS with:
- Grid layout for addon cards
- Hover effects and animations
- Mobile-responsive design
- GitHub-style colors and typography

## URL Structure

### Main Repository URL
```
https://seranov.github.io/kodi-play-random/readme.html
```

OR

```
https://seranov.github.io/kodi-play-random/
```
(This will serve `readme.html` by default if properly configured)

### Addon Download URLs
```
https://seranov.github.io/kodi-play-random/{addon-id}/{addon-id}-{version}.zip
```

Example:
```
https://seranov.github.io/kodi-play-random/context.screenshots/context.screenshots-1.0.5.zip
```

### Documentation URLs
```
https://seranov.github.io/kodi-play-random/doc/{filename}.html
```

Examples:
```
https://seranov.github.io/kodi-play-random/doc/README.html
https://seranov.github.io/kodi-play-random/doc/INSTALLATION.html
```

## For Kodi Integration

The repository can be added to Kodi using the direct repository URL:
```
https://seranov.github.io/kodi-play-random/
```

Kodi will automatically find and parse `addons.xml` to discover available add-ons.

## File Generation Process

### Step-by-step workflow:

1. **Create directories** - Create docs/doc and addon subdirectories
2. **Create ZIP archives** - Package each addon with its assets
3. **Generate addons.xml** - Create repository metadata from addon.xml files
4. **Generate checksum** - Create MD5 hash for validation
5. **Create .nojekyll** - Disable Jekyll to prevent file processing
6. **Convert documentation** - Convert all .md files to .html with styling
7. **Generate readme.html** - Create main landing page with addon cards
8. **Generate index pages** - Create HTML index pages for each addon directory
9. **Deploy to gh-pages** - Push all files to GitHub Pages

## Python Scripts Used

### convert_md_to_html.py
Converts Markdown files to HTML with GitHub-style formatting.

```bash
python3 scripts/convert_md_to_html.py <input_dir> <output_dir>
```

Features:
- Supports both markdown library and fallback basic conversion
- Generates full HTML5 documents
- Adds navigation links
- Applies GitHub-style CSS

### generate_readme.py
Generates readme.html with links to all addons.

```bash
python3 scripts/generate_readme.py <docs_dir>
```

Features:
- Parses addon.xml files
- Extracts addon metadata (name, version, description)
- Creates attractive addon cards
- Includes installation instructions
- Links to documentation

## Customization

### Colors
The readme.html uses a purple gradient:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Modify in the HTML to change color scheme.

### Add-on Display
The addon cards are automatically generated from addon.xml files. To customize:

1. Edit addon.xml in your addon directory
2. Update the `<summary>` and `<description>` tags with lang="en_GB"
3. Re-run the workflow

### Documentation Links
Edit the documentation links section in `generate_readme.py` to add/remove links:

```python
<li><a href="doc/YOURFILE.html">📖 Your Documentation</a></li>
```

## Troubleshooting

### Issue: Addon cards not showing
- Check that addon.xml files exist in addon directories
- Ensure addon directories follow the naming pattern: `plugin.*`, `service.*`, `context.*`, or `repository.*`

### Issue: Documentation not showing
- Check that .md files are in the `/doc` directory
- Ensure Python markdown library is available (optional, falls back to basic conversion)
- Check that HTML files were generated in `docs/doc/`

### Issue: ZIP downloads broken
- Ensure addon ZIP files were created successfully
- Check that addon IDs and versions match between addon.xml and actual files

## GitHub Actions Workflow

The deployment is triggered by:
- Push to main branch
- New version tags (v*)
- Manual workflow_dispatch

The workflow runs in Ubuntu environment and uses:
- Python 3.9+
- rsync for file operations
- zip command for archiving

## Security Notes

- .nojekyll disables Jekyll processing (prevents unwanted file transformations)
- addons.xml.md5 provides checksum verification for Kodi
- All files are served from GitHub Pages (HTTPS by default)
- No server-side processing (static files only)

## Future Enhancements

Possible improvements:
1. Search functionality in readme.html
2. Add-on screenshots/previews
3. Automatic changelog display
4. Multi-language support (i18n)
5. User ratings/reviews
6. Automated changelog generation

## Support

For issues or questions:
- Check GitHub Issues: https://github.com/seranov/seranov-kodi/issues
- Review workflow logs in Actions tab
- Validate addon.xml files with XML validator

