# Installation Guide

> [Русская версия / Russian version](INSTALLATION.ru.md)

## Quick Start

The easiest way to install all add-ons from this repository is to install the repository add-on first.

## Option 1: Install Repository Add-on (Recommended)

1. **Download the repository zip file:**
   - Go to [Releases](https://github.com/seranov/kodi-play-random/releases/latest)
   - Download `repository.seranov-1.0.0.zip`

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

## Option 2: Add Repository Source (For Auto-Updates)

1. **Add file source:**
   - Go to **Settings** → **File manager**
   - Click **Add source**
   - Click **<None>**
   - Enter the URL: `https://raw.githubusercontent.com/seranov/kodi-play-random/main/repo/`
     > **Note:** This URL is intended for use in Kodi. When opened directly in a browser, you may see a 400 error - this is normal. Kodi uses this URL to access the `addons.xml` file and addon ZIP archives.
   - Enter a name: `Seranov Repository`
   - Click **OK**

2. **Install repository from source:**
   - Go to **Add-ons** → **Install from zip file**
   - Select **Seranov Repository** source
   - Select `repository.seranov-1.0.0.zip`
   - Wait for installation confirmation

3. **Install add-ons:**
   - Go to **Add-ons** → **Install from repository**
   - Select **Seranov's Kodi Repository**
   - Browse and install desired add-ons

## Option 3: Install Individual Add-on

If you only want one specific add-on without the repository:

1. Download the specific add-on zip from [Releases](https://github.com/seranov/kodi-play-random/releases/latest)
2. Follow steps 2-3 from Option 1 to install the zip file

**Note:** Without installing the repository, you won't receive automatic updates.

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

**Solution:** 
- Make sure you're using Kodi 19 (Matrix) or later
- Check that all dependencies are available
- Look at the Kodi log file for detailed error messages

### Repository doesn't show any add-ons

**Solution:**
- Make sure you have an internet connection
- Try updating the repository: Right-click on "Seranov's Kodi Repository" and select "Check for updates"

---

## Additional Resources

- [Quick Start Guide](QUICKSTART.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Release Notes](RELEASE_NOTES.md)

