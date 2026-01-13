# Installation Guide

> [Русская версия / Russian version](INSTALLATION.ru.md)

## Quick Start

The easiest way to install all add-ons from this repository is to add the repository URL in Kodi.

## Option 1: Install via File Manager (Recommended)

This method adds the repository as a file source in Kodi, allowing you to browse and install add-ons directly.

### Prerequisites

⚠️ **Important:** First enable installation from unknown sources.

1. **Enable "Unknown sources" in Kodi:**
   - Open Kodi
   - Go to **Settings** (gear icon)
   - Select **System** → **Add-ons**
   - Enable **Unknown sources**
   - Click **Yes** to confirm the warning

### Installation Steps

1. **Add Repository as File Source:**
   - Go to **Settings** → **File manager**
   - Click **Add source**
   - Click **<None>**
   - Enter URL: `https://seranov.github.io/seranov-kodi/`
   - Enter name: `Seranov Repo`
   - Click **OK**

2. **Install Repository:**
   - Go to **Settings** → **Add-ons** → **Install from zip file**
   - Select **Seranov Repo**
   - Navigate to `repository.seranov` folder
   - Select `repository.seranov-1.0.0.zip`
   - Wait for the "Add-on installed" notification

3. **Install Add-ons:**
   - Go to **Add-ons** → **Install from repository**
   - Select **Seranov's Kodi Repository**
   - Choose the category (Video add-ons, Context menus, Services)
   - Install the add-ons you need

### Benefits of URL Installation

✅ **Automatic Updates** - Kodi will automatically check for updates  
✅ **Easy** - No need to download files manually  
✅ **Always Current** - URL always points to the latest version  
✅ **Single Entry Point** - All add-ons available from one repository

## Option 2: Install via Direct URL

This method allows you to install the repository directly from the internet without adding it as a file source.

### Direct ZIP Installation from URL

⚠️ **Important:** First enable installation from unknown sources (see Option 1 above).

1. **Install repository from URL:**
   - Go to **Settings** → **Add-ons** → **Install from zip file**
   - Select **<None>** or enter the path directly
   - Enter the URL:
     ```
     https://seranov.github.io/seranov-kodi/repository.seranov/repository.seranov-1.0.0.zip
     ```
   - Click **OK**
   - Wait for the "Add-on installed" notification

**Repository URL (GitHub Pages):**
```
https://seranov.github.io/seranov-kodi/repository.seranov.zip
```

After installing the repository, all add-ons will receive automatic updates!

## Option 3: Install Repository Add-on from Downloaded ZIP

This is an alternative method if you have issues with online installation.

1. **Download the repository zip file:**
   - Direct link: `https://seranov.github.io/seranov-kodi/repository.seranov.zip`
   - Or go to [Releases](https://github.com/seranov/seranov-kodi/releases/latest)

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

## Option 4: Install Individual Add-on Without Repository

If you only want one specific add-on:

1. Download the specific add-on zip from [Releases](https://github.com/seranov/seranov-kodi/releases/latest):
   - `plugin.video.random.recursive-1.0.0.zip` - Random Player
   - `context.screenshots-1.0.5.zip` - Popup Screenshots
   - `service.seranov.nfoscanner-1.0.0.zip` - NFO Scanner Service
   - `plugin.video.unified.browser-1.0.0.zip` - Unified Browser

2. Follow steps 2-3 from **Option 3** to install the zip file

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

### Files not showing in Kodi

**Cause:** Kodi caches the source content  
**Solution:** 
- Restart Kodi
- Or remove the source and add it again

### 404 error when opening URL

**Cause:** GitHub Pages is not yet deployed or the URL is incorrect  
**Solution:** 
- Use the direct GitHub Pages URL: `https://seranov.github.io/seranov-kodi/repository.seranov.zip`
- Check that you have internet connection
- Try again in a few minutes if GitHub Pages was just deployed

### Add-on installation fails

**Causes and Solutions:**

1. **Internet connection issue**
   - Check your internet connection
   - Try again later

2. **Corrupted download**
   - Make sure the ZIP file was downloaded correctly
   - Try downloading again from [Releases](https://github.com/seranov/seranov-kodi/releases)

3. **Unknown sources disabled**
   - Enable "Unknown sources" in settings (see Option 1, Step 1)

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

