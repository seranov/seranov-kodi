# Installation Guide

> [Русская версия / Russian version](INSTALLATION.ru.md)

## Quick Start

The easiest way to install all add-ons from this repository is to add the repository URL in Kodi.

## Option 1: Install via GitHub Pages URL (Easiest)

⚠️ **Requirement:** GitHub Pages must be activated for the repository.

### Direct Installation via File Manager

1. Open Kodi
2. Go to **Settings** (gear icon) → **File manager**
3. Click **Add source**
4. Click on **<None>** and enter the URL:
   ```
   https://seranov.github.io/seranov-kodi/
   ```
5. Enter a name for the source (e.g., `Seranov Repo`)
6. Click **OK**
7. Return to the home screen
8. Go to **Settings** → **Add-ons** → **Install from zip file**
9. Select `Seranov Repo`
10. Select `repository.seranov/repository.seranov-1.0.0.zip`
11. Wait for the "Add-on installed" notification

After installing the repository, all add-ons will receive automatic updates!

## Option 2: Install Repository Add-on from Downloaded ZIP

This is an alternative method if you have issues with online installation.

1. **Download the repository zip file:**
   - Go to [Releases](https://github.com/seranov/seranov-kodi/releases/latest)
   - Download `repository.seranov-1.0.0.zip`
   
   **Direct links:**
   - Always available: `https://github.com/seranov/seranov-kodi/raw/main/repo/repository.seranov/repository.seranov-1.0.0.zip`
   - Via GitHub Pages (after activation): `https://seranov.github.io/seranov-kodi/repository.seranov/repository.seranov-1.0.0.zip`

2. **Enable "Unknown sources" in Kodi:**
   - Open Kodi **Settings** (gear icon)
   - Go to **System** → **Add-ons**
   - Enable **Unknown sources**
   - Click **Yes** to confirm the warning

3. **Install the repository:**
   - Go to **Add-ons** menu (puzzle piece icon)
   - Click the **box icon** at the top left
   - Select **Install from zip file**
   - Navigate to where you downloaded `repository.seranov-1.0.0.zip`
   - Select the file and wait for the "Add-on installed" notification

4. **Install add-ons from the repository:**
   - Go to **Add-ons** menu
   - Click the **box icon** at the top left
   - Select **Install from repository**
   - Select **Seranov's Kodi Repository**
   - Choose the category (Video add-ons, Context menus, Services)
   - Select the add-on you want to install
   - Click **Install**

## Option 3: Install Individual Add-on Without Repository

If you only want one specific add-on:

1. Download the specific add-on zip from [Releases](https://github.com/seranov/seranov-kodi/releases/latest):
   - `plugin.video.random.recursive-1.0.0.zip` - Random Player
   - `context.screenshots-1.0.5.zip` - Popup Screenshots
   - `service.seranov.nfoscanner-1.0.0.zip` - NFO Scanner Service
   - `plugin.video.unified.browser-1.0.0.zip` - Unified Browser

2. Follow steps 2-3 from **Option 2** to install the zip file

**⚠️ Important:** Without installing the repository, you won't receive automatic updates.

## Automatic Updates

> **✅ Now Available:** The repository is published via GitHub Pages and supports automatic updates!

After installing the repository add-on (Option 1), Kodi will automatically check for updates to all installed add-ons.

**Repository URL:** `https://seranov.github.io/seranov-kodi/`

### How Automatic Updates Work

1. **Install the repository once** using the ZIP file
2. **Kodi checks for updates** automatically (usually every 24 hours)
3. **You get notified** when updates are available
4. **Install updates** with one click from the add-ons menu

### Manual Update Check

To manually check for updates:
1. Go to **Add-ons** menu
2. Right-click on **Seranov's Kodi Repository**
3. Select **Check for updates**

---

## Available Add-ons

### Repository
- **File:** `repository.seranov-1.0.0.zip`
- Install this first for easy access to all other add-ons

### Random Recursive Video Player
- **File:** `plugin.video.random.recursive-1.0.0.zip`
- Play videos recursively in random order

### Unified Video Browser
- **File:** `plugin.video.unified.browser-1.0.0.zip`
- Browse all videos in a unified interface

### Popup Screenshots
- **File:** `context.screenshots-1.0.5.zip`
- Display screenshots in a slideshow

### NFO Scanner Service
- **File:** `service.seranov.nfoscanner-1.0.0.zip`
- Background NFO file scanner

---

## Troubleshooting

### "Install from zip file" option is greyed out

**Solution:** You need to enable "Unknown sources" in Settings → System → Add-ons

### Add-on installation fails

**Causes and Solutions:**

1. **Internet connection issue**
   - Check your internet connection
   - Try again later

2. **Corrupted download**
   - Make sure the ZIP file was downloaded correctly
   - Try downloading again from [Releases](https://github.com/seranov/seranov-kodi/releases)

3. **Unknown sources disabled**
   - Enable "Unknown sources" in settings (see Option 1, Step 2)

4. **Outdated Kodi version**
   - Update Kodi to version 19.x or later

### Repository doesn't show any add-ons

**Solution:**
- Make sure you have an internet connection
- Try updating the repository: Right-click on "Seranov's Kodi Repository" and select "Check for updates"

---

## Additional Resources

- [Quick Start Guide](QUICKSTART.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Release Notes](RELEASE_NOTES.md)

