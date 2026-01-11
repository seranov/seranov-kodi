# GitHub Pages Deployment Configuration Update
Date: 2026-01-11

## Overview
Updated the GitHub Pages deployment pipeline to:
1. Remove default index.html page
2. Deploy unpacked Kodi addon repository files to the root
3. Convert MD documentation to HTML
4. Generate readme.html with plugin links and descriptions

## Changes Made

### 1. Python Scripts Created

#### `scripts/convert_md_to_html.py`
Converts Markdown documentation files to HTML with styling.
- Supports both markdown library and fallback basic conversion
- Applies GitHub-flavored Markdown styling
- Creates properly formatted HTML documents with navigation
- Handles all markdown files in the doc directory

**Features:**
- Full HTML5 document generation with responsive CSS
- GitHub-style code highlighting and formatting
- Automatic back-to-home navigation links
- Proper indentation and readable HTML output
- Handles headers, bold, italic, links, code blocks, blockquotes, tables
- Mobile-responsive design with viewport meta tags

**Usage:**
```bash
python3 scripts/convert_md_to_html.py <input_dir> <output_dir>
```

**Example:**
```bash
python3 scripts/convert_md_to_html.py doc docs/doc
```

#### `scripts/generate_readme.py`
Generates readme.html with links to all plugins and their descriptions.
- Parses addon.xml files to extract metadata
- Creates attractive HTML cards for each addon
- Includes installation instructions
- Links to documentation pages
- Responsive grid layout for addon display

**Features:**
- Scans addons in docs directory automatically
- Extracts summaries and descriptions from addon.xml (English versions)
- Creates downloadable ZIP links with version information
- Responsive grid layout (auto-fill columns)
- Modern gradient background design
- Two installation methods documented
- Direct repository URL for Kodi integration
- Animated hover effects on addon cards

**Usage:**
```bash
python3 scripts/generate_readme.py <docs_dir>
```

**Example:**
```bash
python3 scripts/generate_readme.py docs
```

### 2. GitHub Actions Workflow Updated

File: `.github/workflows/publish-release.yml`

#### Changes:
- **Step 3**: Added `docs/doc` directory creation for documentation
- **Step 7**: Changed to create `.nojekyll` file (disables Jekyll processing)
- **Step 8**: New step to convert Markdown to HTML
- **Step 9**: New step to generate readme.html
- **Step 10**: Generate addon index pages (previously step 8)
- All subsequent steps renumbered accordingly

#### Complete Workflow Steps:

1. **Checkout repository** - Fetch all branches and history
2. **Setup Python** - Install Python 3.9+ (required for scripts)
3. **Create output directories** - Prepare docs and docs/doc
4. **Create addon ZIP archives** - Package all addons with assets
5. **Generate addons.xml** - Create repository metadata file
6. **Generate addons.xml.md5** - Create checksum for validation
7. **Create .nojekyll file** - Disable Jekyll processing
8. **Convert documentation** - Run convert_md_to_html.py
9. **Generate readme.html** - Run generate_readme.py
10. **Generate addon index pages** - Create HTML directory listings
11. **Display output structure** - Show what was generated
12. **Configure GitHub Pages** - Set up GitHub Pages settings
13. **Deploy to GitHub Pages** - Push to gh-pages branch
14. **Deployment complete** - Print success message

#### Deployment Structure

**Before:**
```
docs/
  ├── index.html (default page)
  ├── addons.xml
  ├── addons.xml.md5
  ├── addon-dirs/
  │   ├── zip files
  │   └── icon files
```

**After:**
```
docs/
  ├── .nojekyll (no Jekyll processing)
  ├── readme.html (main landing page)
  ├── addons.xml
  ├── addons.xml.md5
  ├── doc/
  │   ├── README.html
  │   ├── QUICKSTART.html
  │   ├── INSTALLATION.html
  │   ├── CONTRIBUTING.html
  │   └── other docs...
  ├── addon-dirs/
  │   ├── zip files
  │   └── icon files
  └── [addon-directories]/
      └── index.html (for each addon)
```

## Key Features

### readme.html
- **Modern, responsive design** with gradient background (purple #667eea to #764ba2)
- **Cards for each addon** with:
  - 📦 Addon icon
  - Name and version
  - English summary (bold text)
  - English description
  - Download ZIP button (primary button)
  - View Files link (secondary button)
  
- **Grid layout**:
  - Auto-fill columns (minmax 350px)
  - 20px gap between cards
  - Responsive on mobile and desktop
  
- **Hover animations**:
  - Cards lift up (translateY -5px)
  - Shadow effects
  - Link color changes
  
- **Installation instructions**:
  - Method 1: Install repository (recommended)
  - Method 2: Direct ZIP installation
  - Step-by-step guides with numbered lists
  
- **Documentation links section**:
  - Grid layout for links
  - Icons for each doc type
  - Links to all converted HTML docs
  
- **Repository information**:
  - Direct repository URL for Kodi
  - Links to addons.xml and checksum
  - Footer with GitHub and Kodi links

### Documentation HTML Pages
- **GitHub-style formatting**:
  - Color scheme matches GitHub (#24292e, #666)
  - Code highlighting with monospace fonts
  - Proper heading hierarchy
  - Link colors (#0366d6)
  - Table formatting with borders
  - Block quotes with left border
  
- **Responsive design**:
  - Max-width 900px for readability
  - Mobile viewport support
  - Proper padding and margins
  
- **Navigation**:
  - Back to home link at top
  - Consistent styling across all pages
  - Readable line heights (1.6)

### Addon Discovery
- **Automatic detection** of all addons in docs directory
- **Pattern matching**: `plugin.*`, `service.*`, `context.*`, `repository.*`
- **Metadata extraction** from source addon.xml files (not copies)
- **Shows both English summaries and descriptions**
- **Provides version information**
- **Creates direct download links** with proper paths

## Installation Instructions

The readme.html includes two installation methods:

### Method 1: Repository Method (Recommended)
1. Download repository.seranov ZIP
2. In Kodi: Add-ons → Install from zip file
3. Select downloaded ZIP
4. Wait for installation
5. Access add-ons from Kodi's repository

### Method 2: Direct ZIP Method
1. Download individual addon ZIP
2. In Kodi: Add-ons → Install from zip file
3. Select downloaded ZIP
4. Wait for installation

## Documentation Access

All documentation is now accessible via:

```
https://seranov.github.io/seranov-kodi/readme.html     (main page)
https://seranov.github.io/seranov-kodi/doc/README.html
https://seranov.github.io/seranov-kodi/doc/QUICKSTART.html
https://seranov.github.io/seranov-kodi/doc/INSTALLATION.html
https://seranov.github.io/seranov-kodi/doc/CONTRIBUTING.html
https://seranov.github.io/seranov-kodi/doc/RELEASE_NOTES.html
```

## URLs

### Main Repository Page
```
https://seranov.github.io/seranov-kodi/readme.html
```

### Direct Repository URL (for Kodi)
```
https://seranov.github.io/seranov-kodi/
```

### Addon Download Examples
```
https://seranov.github.io/seranov-kodi/context.screenshots/context.screenshots-1.0.5.zip
https://seranov.github.io/seranov-kodi/plugin.video.unified.browser/plugin.video.unified.browser-1.0.0.zip
```

## Technical Details

### Dependencies
- Python 3.9+ (already required by workflow)
- Optional: markdown library for enhanced MD to HTML conversion
- Falls back to basic regex conversion if markdown library unavailable

### Workflow Execution
The deployment occurs on:
- Push to main branch
- New version tags (v*)
- Manual workflow dispatch

### Files Generated
1. `addons.xml` - Repository metadata
2. `addons.xml.md5` - Checksum for validation
3. `readme.html` - Landing page with addon cards
4. `doc/*.html` - Converted documentation files
5. Addon-specific index pages for directory browsing
6. `.nojekyll` - Jekyll disable file

### Triggers
- Push to `main` branch
- Tags matching `v*` (e.g., v1.0.0)
- Manual trigger via workflow_dispatch

## Benefits

1. **Better User Experience**:
   - Modern, responsive design
   - Easy navigation
   - Clear installation instructions
   
2. **Automatic Documentation**:
   - No manual HTML conversion needed
   - Consistent styling across all docs
   - Automatic back-links
   
3. **Discoverable Addons**:
   - Clear cards with descriptions
   - Direct download links
   - Version information visible
   
4. **Multiple Installation Methods**:
   - Users can choose preferred method
   - Both Kodi and direct methods documented
   
5. **Clean Repository URL**:
   - Works with Kodi's repository system
   - Direct access to all files
   - No Jekyll interference (.nojekyll)
   
6. **Self-Documenting**:
   - readme.html serves as standalone guide
   - No external dependencies needed
   - Static files only (secure, fast)

## Files Added/Modified

### New Files
- `scripts/convert_md_to_html.py` - Markdown to HTML converter
- `scripts/generate_readme.py` - readme.html generator
- `doc/GITHUB_PAGES_GUIDE.md` - User guide for GitHub Pages
- `doc/PYTHON_SCRIPTS_GUIDE.md` - Developer documentation for scripts
- `doc/report/2026-01-11-github-pages-deployment-update.md` - This report

### Modified Files
- `.github/workflows/publish-release.yml` - Updated with new steps

## Testing

### Local Testing
```bash
# Test Markdown conversion
python3 scripts/convert_md_to_html.py doc test_output
ls test_output/

# Test readme generation
python3 scripts/generate_readme.py docs
cat docs/readme.html
```

### Validation
- Check generated HTML files in browser
- Validate HTML5 syntax at validator.w3.org
- Test addon download links
- Verify CSS rendering on mobile devices

## Future Enhancements

Possible improvements:
- Add search functionality to readme.html
- Include screenshots/previews for addons
- Create changelog display for each addon
- Create language-specific pages (i18n)
- Add rating/review system
- Automated changelog generation from git commits
- Dark mode support
- Add donation/sponsor links
- Create API endpoint for addon discovery
- Add metrics/analytics

## Deployment Verification

After workflow completes:

1. Check GitHub Pages settings are configured
2. Visit https://seranov.github.io/seranov-kodi/readme.html
3. Verify addon cards display correctly
4. Test addon download links
5. Check documentation links
6. Validate in Kodi (add repository URL)

## Support & Documentation

Users can reference:
- `doc/GITHUB_PAGES_GUIDE.md` - How the system works
- `doc/PYTHON_SCRIPTS_GUIDE.md` - Technical details for developers
- Embedded comments in Python scripts
- GitHub Actions logs for deployment details

## Completion Status

✅ All required changes implemented:
- ✅ Removed default index.html
- ✅ Created readme.html with addon cards
- ✅ Converted documentation to HTML
- ✅ Added .nojekyll file
- ✅ Created Python conversion scripts
- ✅ Updated GitHub Actions workflow
- ✅ Created documentation for users and developers

The GitHub Pages site is now fully configured and ready for deployment!

