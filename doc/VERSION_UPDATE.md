# Kodi Plugin Version Update Guide

> [Русская версия / Russian version](VERSION_UPDATE.ru.md)

This guide explains step-by-step how to properly update Kodi plugin versions in the source code, compile them, and publish them so that Kodi automatically detects and installs updates.

## Table of Contents

- [Process Overview](#process-overview)
- [Prerequisites](#prerequisites)
- [Step 1: Update Version in Source Code](#step-1-update-version-in-source-code)
- [Step 2: Local Testing](#step-2-local-testing)
- [Step 3: Publish Changes](#step-3-publish-changes)
- [Step 4: Automatic Build and Deploy](#step-4-automatic-build-and-deploy)
- [Step 5: Verify Update in Kodi](#step-5-verify-update-in-kodi)
- [How Automatic Updates Work](#how-automatic-updates-work)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

---

## Process Overview

The plugin update process consists of the following stages:

1. **Code Changes** → Make changes to the plugin code
2. **Version Update** → Change the version number in `addon.xml`
3. **Local Testing** → Verify functionality locally
4. **Commit and Push** → Send changes to GitHub
5. **Automatic Build** → GitHub Actions creates ZIP archives
6. **Automatic Deploy** → Publish to GitHub Pages
7. **Kodi Update** → Kodi automatically detects the new version

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│    Code     │ --> │   Version    │ --> │     Local     │
│   Changes   │     │    Update    │     │    Testing    │
└─────────────┘     └──────────────┘     └───────────────┘
                                                  │
                                                  ▼
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│    Kodi     │ <-- │    GitHub    │ <-- │  git push     │
│   Updates   │     │    Pages     │     │    origin     │
│   Plugin    │     │ (automatic)  │     │     main      │
└─────────────┘     └──────────────┘     └───────────────┘
```

---

## Prerequisites

### For Development

- **Git** - for working with the repository
- **Python 3.9+** - for local build testing
- **Text Editor** - VS Code, PyCharm, Sublime Text, etc.
- **Kodi** - for plugin testing

### For Automatic Publishing

- **GitHub Pages** - must be enabled in repository settings
- **GitHub Actions** - must be active (enabled by default)
- **Access Rights** - write permissions to the repository

### Understanding Semantic Versioning

Plugin versions follow the `MAJOR.MINOR.PATCH` format:

- **MAJOR** (1.x.x) - Breaking changes, incompatible with previous versions
- **MINOR** (x.1.x) - New features, backward compatible
- **PATCH** (x.x.1) - Bug fixes, minor improvements

**Examples:**
- `1.0.0` → `1.0.1` - Fixed a bug
- `1.0.1` → `1.1.0` - Added a new feature
- `1.1.0` → `2.0.0` - API changed, incompatible with 1.x

---

## Step 1: Update Version in Source Code

### 1.1. Find the addon.xml File

Each plugin has an `addon.xml` file in the plugin's root directory:

```
plugin.video.random.recursive/
├── addon.xml              ← Version is here
├── main.py
├── icon.png
└── resources/
```

### 1.2. Open the addon.xml File

**Example content:**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="plugin.video.random.recursive" 
       name="Bidon Random Recursive Player" 
       version="1.0.0" 
       provider-name="seranov">
    <requires>
        <import addon="xbmc.python" version="3.0.0"/>
    </requires>
    ...
</addon>
```

### 1.3. Change the Version Number

Find the `version` attribute in the `<addon>` tag and change it to the new version number:

**Before:**
```xml
<addon id="plugin.video.random.recursive" 
       name="Bidon Random Recursive Player" 
       version="1.0.0" 
       provider-name="seranov">
```

**After:**
```xml
<addon id="plugin.video.random.recursive" 
       name="Bidon Random Recursive Player" 
       version="1.0.1" 
       provider-name="seranov">
```

### 1.4. Update Changelog (optional but recommended)

If your plugin has a `changelog.txt` file, add a description of the changes:

```
v1.0.1 (2026-01-07)
- Fixed video playback bug
- Improved handling of Cyrillic paths
- Optimized performance with large libraries

v1.0.0 (2026-01-01)
- Initial release
```

### 1.5. Save Changes

Save the `addon.xml` file and all modified plugin code files.

---

## Step 2: Local Testing

### 2.1. Verify addon.xml Correctness

Make sure the XML file is syntactically correct:

```bash
# Linux/Mac
xmllint --noout plugin.video.random.recursive/addon.xml

# Windows (PowerShell)
# Open the file in a browser - if it opens without errors, the XML is valid
```

### 2.2. Build Repository Locally (optional)

You can test the build process locally before publishing:

**Windows (PowerShell):**
```powershell
cd C:\prj\seranov-kodi
.\scripts\build-release.ps1
```

**Linux/Mac:**
```bash
cd ~/seranov-kodi
python3 scripts/generate_repo.py
```

This will create:
- Plugin ZIP archive in `repo/plugin.video.random.recursive/`
- Updated `repo/addons.xml` file
- Checksum `repo/addons.xml.md5`

### 2.3. Test Plugin in Kodi

**Option 1: Install from ZIP Archive**

1. Copy the generated ZIP from `repo/plugin.video.random.recursive/plugin.video.random.recursive-1.0.1.zip`
2. In Kodi: **Add-ons** → **Install from zip file**
3. Select the copied ZIP file
4. Verify plugin functionality

**Option 2: Direct Deployment (Windows only)**

```powershell
# Automatic copy to Kodi directory
.\scripts\deploy-local.ps1 -AddonsToDeploy @('plugin.video.random.recursive')
```

### 2.4. Verify Functionality

- Ensure the plugin starts without errors
- Test all new features
- Verify that fixed bugs are actually fixed

---

## Step 3: Publish Changes

### 3.1. Check Git Status

```bash
cd /home/runner/work/seranov-kodi/seranov-kodi
git status
```

You should see modified files:
```
modified:   plugin.video.random.recursive/addon.xml
modified:   plugin.video.random.recursive/main.py
```

### 3.2. Add Changes to Git

```bash
# Add specific files
git add plugin.video.random.recursive/addon.xml
git add plugin.video.random.recursive/main.py

# Or add the entire plugin directory
git add plugin.video.random.recursive/

# Or add all modified files
git add .
```

### 3.3. Create Commit with Descriptive Message

**A good commit message should:**
- Indicate the new version number
- Briefly describe what changed
- Be in English (recommended for open projects)

**Examples of good commit messages:**

```bash
# Simple fix
git commit -m "plugin.video.random.recursive: bump to v1.0.1 - fix video playback"

# Multiple changes
git commit -m "plugin.video.random.recursive: bump to v1.1.0

- Add support for subtitle auto-loading
- Fix cyrillic paths handling
- Improve performance with large libraries
- Update Russian translations"

# With change type indicator
git commit -m "fix(random.recursive): bump to v1.0.1 - resolve playback issues"
```

### 3.4. Push Changes to GitHub

```bash
git push origin main
```

If you're working in a separate branch:
```bash
git push origin feature/version-1.0.1
```

Then create a Pull Request in the GitHub web interface.

---

## Step 4: Automatic Build and Deploy

After changes reach the `main` branch, an automatic process starts:

### 4.1. GitHub Actions Automatically Triggers

The workflow `.github/workflows/publish-release.yml` activates automatically on:
- Push to `main` branch
- Creating a tag like `v*` (e.g., `v1.0.1`)
- Manual trigger via web interface

### 4.2. What GitHub Actions Does

**Automatic build steps:**

1. **Checkout repository** - downloads code
2. **Setup Python 3.9** - configures environment
3. **Create directory structure** - creates `docs/` and subdirectories
4. **Create ZIP archives** - packages each plugin into a separate ZIP
   ```
   docs/
   └── plugin.video.random.recursive/
       ├── plugin.video.random.recursive-1.0.1.zip
       └── icon.png
   ```
5. **Generate addons.xml** - creates repository metadata
6. **Generate addons.xml.md5** - creates checksum
7. **Create index.html** - creates web pages for convenient viewing
8. **Deploy to GitHub Pages** - publishes to `gh-pages` branch

### 4.3. Monitor Progress

**Track build status here:**

1. Go to Actions page: https://github.com/seranov/seranov-kodi/actions
2. Find the latest workflow run "Publish Kodi Repository"
3. Open it and check the status of each step

**Workflow statuses:**
- 🟡 **Yellow (In Progress)** - Build is running
- 🟢 **Green (Success)** - Build successful, plugin published
- 🔴 **Red (Failed)** - Build error, check logs

### 4.4. Verify Deployment

After successful build (usually 1-3 minutes), verify files are accessible:

```bash
# Check addons.xml
curl https://seranov.github.io/seranov-kodi/addons.xml

# Check ZIP archive
curl -I https://seranov.github.io/seranov-kodi/plugin.video.random.recursive/plugin.video.random.recursive-1.0.1.zip
```

Or open in browser:
- https://seranov.github.io/seranov-kodi/
- https://seranov.github.io/seranov-kodi/addons.xml

**Important:** GitHub Pages updates may take 5-10 minutes due to CDN caching.

---

## Step 5: Verify Update in Kodi

### 5.1. Automatic Update Check

Kodi automatically checks for repository updates:
- Periodically (default every 24 hours)
- On Kodi startup
- On manual check

### 5.2. Manual Update Check

To see the update immediately:

1. Open Kodi
2. Go to **Add-ons**
3. Find **Seranov's Kodi Repository**
4. Right-click → **Check for updates**

### 5.3. Install Update

If an update is found:

1. Kodi will show notification: "Updates available"
2. Go to **Add-ons** → **My add-ons**
3. Find plugin with available update (marked with icon)
4. Click → **Update**

Or:
1. **System** → **Settings** → **Add-ons**
2. **Updates** → Enable automatic updates
3. Kodi will update plugins automatically

### 5.4. Verify Installed Version

After update, verify version:

1. **Add-ons** → **My add-ons**
2. Select plugin
3. Open **Information**
4. Check version number - should be `1.0.1`

---

## How Automatic Updates Work

### Update System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        GitHub                                │
│  ┌────────────────┐        ┌─────────────────┐              │
│  │  Repository    │ push   │  GitHub Actions │              │
│  │   (main)       │───────>│   Workflow      │              │
│  └────────────────┘        └────────┬────────┘              │
│                                     │                        │
│                                     │ deploy                 │
│                                     ▼                        │
│                            ┌─────────────────┐               │
│                            │  GitHub Pages   │               │
│                            │   (gh-pages)    │               │
│                            └────────┬────────┘               │
└─────────────────────────────────────┼───────────────────────┘
                                      │
                                      │ HTTPS
                                      ▼
                    ┌─────────────────────────────────┐
                    │  https://seranov.github.io/     │
                    │       seranov-kodi/             │
                    │                                 │
                    │  ├── addons.xml                 │
                    │  ├── addons.xml.md5             │
                    │  └── plugin.../plugin....zip    │
                    └────────┬────────────────────────┘
                             │
                             │ check every 24 hours
                             ▼
                    ┌─────────────────┐
                    │      Kodi       │
                    │   (user device) │
                    └─────────────────┘
```

### How Kodi Discovers Updates

1. **Repository installed** - User has `repository.seranov` installed
2. **Repository URL** - In `repository.seranov/addon.xml` the URL is specified:
   ```xml
   <datadir>https://seranov.github.io/seranov-kodi/</datadir>
   ```
3. **Periodic check** - Kodi periodically:
   - Downloads `addons.xml` from the specified URL
   - Compares versions in `addons.xml` with installed versions
   - If version in `addons.xml` is higher - update available
4. **Notification** - Kodi shows update notification
5. **Installation** - With user consent, Kodi:
   - Downloads plugin ZIP archive from GitHub Pages
   - Extracts it to its plugins directory
   - Reloads the plugin

### Files Responsible for Updates

**repository.seranov/addon.xml:**
```xml
<extension point="xbmc.addon.repository" name="Seranov's Kodi Repository">
    <info compressed="false">https://seranov.github.io/seranov-kodi/addons.xml</info>
    <checksum>https://seranov.github.io/seranov-kodi/addons.xml.md5</checksum>
    <datadir zip="true">https://seranov.github.io/seranov-kodi/</datadir>
</extension>
```

- **info** - URL of file with all plugin metadata
- **checksum** - URL of checksum for integrity verification
- **datadir** - Base URL for downloading ZIP archives

**addons.xml:**
```xml
<addons>
    <addon id="plugin.video.random.recursive" version="1.0.1" ...>
        ...
    </addon>
    <addon id="context.screenshots" version="1.0.5" ...>
        ...
    </addon>
    ...
</addons>
```

This file contains current versions of all plugins. Kodi compares versions from this file with locally installed ones.

---

## Troubleshooting

### Problem: GitHub Actions Doesn't Start

**Check:**
1. GitHub Actions enabled: Settings → Actions → General → Allow all actions
2. Workflow file exists: `.github/workflows/publish-release.yml`
3. Push was to `main` branch (not another branch)

**Solution:**
```bash
# Manual workflow trigger
# Go to: https://github.com/seranov/seranov-kodi/actions
# Select "Publish Kodi Repository" → Run workflow
```

### Problem: Build Failed with Error

**Common causes:**
- Syntax error in `addon.xml`
- Missing required file (icon.png, addon.xml)
- Invalid version format (should be X.Y.Z)

**Solution:**
1. Open GitHub Actions logs
2. Find the error line (usually in red)
3. Fix the error
4. Make a new commit and push

**Check XML locally:**
```bash
xmllint --noout plugin.video.random.recursive/addon.xml
```

### Problem: GitHub Pages Not Updating

**Possible causes:**
1. CDN caching (usually clears in 5-10 minutes)
2. gh-pages branch doesn't exist or is empty
3. GitHub Pages not configured

**Check:**
```bash
# Check gh-pages branch
git ls-remote origin gh-pages

# Check contents
# https://github.com/seranov/seranov-kodi/tree/gh-pages
```

**Solution:**
1. Wait 10 minutes for CDN update
2. Check Settings → Pages → Source = gh-pages branch
3. Try in browser incognito mode (bypass local cache)

### Problem: Kodi Doesn't See Update

**Causes:**
1. GitHub Pages hasn't updated yet (wait 10 minutes)
2. Kodi hasn't checked for updates yet
3. Version in Kodi is already higher or equal

**Solution:**
1. Verify `addons.xml` contains new version:
   ```bash
   curl https://seranov.github.io/seranov-kodi/addons.xml | grep plugin.video.random.recursive
   ```
2. Force update check in Kodi:
   - Right-click on repository → Check for updates
3. Check installed version:
   - My add-ons → Plugin → Information

### Problem: Error Installing Update in Kodi

**Causes:**
1. ZIP file corrupted or unavailable
2. Insufficient write permissions
3. Dependency conflict

**Solution:**
1. Check ZIP availability:
   ```bash
   curl -I https://seranov.github.io/seranov-kodi/plugin.video.random.recursive/plugin.video.random.recursive-1.0.1.zip
   ```
2. Check Kodi log:
   - Windows: `%APPDATA%\Kodi\kodi.log`
   - Linux: `~/.kodi/temp/kodi.log`
   - Mac: `~/Library/Logs/kodi.log`
3. Try reinstalling plugin:
   - Remove current version
   - Install new version from ZIP manually

---

## Examples

### Example 1: Bug Fix (patch version)

**Scenario:** Bug discovered in video playback with Cyrillic paths

**Steps:**

1. Fix code in `main.py`:
```python
# Before
video_path = path

# After
video_path = path.encode('utf-8').decode('utf-8')
```

2. Update version `1.0.0` → `1.0.1` in `addon.xml`:
```xml
<addon id="plugin.video.random.recursive" version="1.0.1" ...>
```

3. Commit and push:
```bash
git add plugin.video.random.recursive/
git commit -m "plugin.video.random.recursive: bump to v1.0.1 - fix cyrillic paths"
git push origin main
```

4. Wait ~2 minutes for GitHub Actions to complete
5. Check in Kodi after 10 minutes

### Example 2: New Feature (minor version)

**Scenario:** Added automatic subtitle loading support

**Steps:**

1. Add new code in `main.py`:
```python
def load_subtitles(video_path):
    # New function
    subtitle_path = video_path.rsplit('.', 1)[0] + '.srt'
    if os.path.exists(subtitle_path):
        return subtitle_path
    return None
```

2. Update version `1.0.1` → `1.1.0` in `addon.xml`:
```xml
<addon id="plugin.video.random.recursive" version="1.1.0" ...>
```

3. Update changelog.txt:
```
v1.1.0 (2026-01-10)
+ Added automatic subtitle loading
- Fixed Cyrillic paths bug (from v1.0.1)

v1.0.1 (2026-01-07)
- Fixed Cyrillic paths bug

v1.0.0 (2026-01-01)
- Initial release
```

4. Commit and push:
```bash
git add plugin.video.random.recursive/
git commit -m "plugin.video.random.recursive: bump to v1.1.0

- Add automatic subtitle loading support
- Subtitles are auto-loaded if .srt file exists
- Updated documentation"
git push origin main
```

### Example 3: Multiple Plugin Update

**Scenario:** Update two plugins in one release

**Steps:**

1. Update first plugin:
```bash
# Change plugin.video.random.recursive/addon.xml
version="1.1.0"
```

2. Update second plugin:
```bash
# Change context.screenshots/addon.xml
version="1.0.6"
```

3. Commit and push:
```bash
git add plugin.video.random.recursive/ context.screenshots/
git commit -m "Release multiple addons

- plugin.video.random.recursive: v1.1.0 - Add subtitle support
- context.screenshots: v1.0.6 - Fix image loading issue"
git push origin main
```

4. GitHub Actions will build both plugins in one run

### Example 4: Create Git Tag for Release (optional)

**Scenario:** Create tag for important release

**Steps:**

1. After version update and push to main:
```bash
git checkout main
git pull origin main
```

2. Create annotated tag:
```bash
git tag -a v1.1.0 -m "Release v1.1.0

Major changes:
- plugin.video.random.recursive v1.1.0: Subtitle support
- context.screenshots v1.0.6: Image loading fix
- Updated documentation"
```

3. Push tag to GitHub:
```bash
git push origin v1.1.0
```

4. Create GitHub Release (optional):
   - Go to: https://github.com/seranov/seranov-kodi/releases/new
   - Select tag: `v1.1.0`
   - Fill description
   - Attach ZIP files (optional)
   - Click "Publish release"

---

## Additional Resources

### Internal Documentation
- [BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md) - Detailed build guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - Release notes
- [README.md](README.md) - Main page

### External Links
- [Kodi Add-on Development](https://kodi.wiki/view/Add-on_development) - Official Kodi documentation
- [Semantic Versioning](https://semver.org/) - Versioning standard
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - GitHub Actions docs
- [GitHub Pages Documentation](https://docs.github.com/en/pages) - GitHub Pages docs

### Scripts in Repository
- `scripts/generate_repo.py` - Python script for repository generation
- `scripts/build-release.ps1` - PowerShell build script (Windows)
- `scripts/deploy-local.ps1` - PowerShell local deployment script
- `.github/workflows/publish-release.yml` - GitHub Actions workflow

---

## Support

If you have questions or issues:

1. **Check documentation:** [doc/](../doc/)
2. **GitHub Issues:** [github.com/seranov/seranov-kodi/issues](https://github.com/seranov/seranov-kodi/issues)
3. **Email:** seranov@yandex.ru

---

**Last Updated:** 2026-01-07
