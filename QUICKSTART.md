# Quick Start Guide

This guide will help you quickly get started with using the Seranov's Kodi repository and service plugins.

## Installation

### Installing the Repository

1. **Download the repository addon:**
   - Go to the [releases](https://github.com/seranov/kodi-play-random/releases) or the `repo` directory
   - Download `repository.seranov-1.0.0.zip`

2. **Install in Kodi:**
   - Open Kodi
   - Go to **Settings** (gear icon) → **Add-ons**
   - Click **Install from zip file**
   - Navigate to the downloaded `repository.seranov-1.0.0.zip`
   - Wait for the "Add-on installed" notification

3. **Browse available add-ons:**
   - Go to **Settings** → **Add-ons** → **Install from repository**
   - Select **Seranov's Kodi Repository**
   - Browse categories to find available add-ons

### Installing Individual Service Plugins

If you want to install a service plugin without the repository:

1. Download the service plugin zip file (e.g., `service.seranov.template1-1.0.0.zip`)
2. In Kodi, go to **Settings** → **Add-ons** → **Install from zip file**
3. Navigate to the downloaded zip file and install

## Using Service Plugins

### Service Template 1

A basic background service that runs periodically.

**Configuration:**
1. Go to **Settings** → **Add-ons** → **My Add-ons** → **Services**
2. Select **Service Template 1**
3. Click **Configure**
4. Adjust settings:
   - **Check interval**: How often the service runs (in seconds)
   - **Enable notifications**: Show notifications
   - **Debug mode**: Enable detailed logging

**What it does:**
- Runs in the background
- Executes tasks at the specified interval
- Can be customized to perform any periodic task

### Service Template 2

An advanced service that monitors Kodi events.

**Configuration:**
1. Go to **Settings** → **Add-ons** → **My Add-ons** → **Services**
2. Select **Service Template 2**
3. Click **Configure**
4. Adjust settings:
   - **Enable playback monitoring**: Monitor when media plays/stops
   - **Enable notifications**: Show notifications
   - **Debug mode**: Enable detailed logging

**What it does:**
- Monitors playback events (play, stop)
- Reacts to Kodi notifications
- Can be extended to handle various Kodi events

### Enabling/Disabling Services

To enable or disable a service:
1. Go to **Settings** → **Add-ons** → **My Add-ons** → **Services**
2. Select the service
3. Click **Enable** or **Disable**

### Viewing Service Logs

To check if a service is working correctly:

1. Enable **Debug logging**:
   - Go to **Settings** → **System** → **Logging**
   - Enable **Enable debug logging**

2. View the log file:
   - **Linux/macOS**: `~/.kodi/temp/kodi.log`
   - **Windows**: `%APPDATA%\Kodi\kodi.log`
   - **Android**: Use a log viewer app or adb

3. Look for messages from your service:
   ```
   [service.seranov.template1] Service Template 1 v1.0.0 started
   [service.seranov.template1] Service is running...
   ```

## Developing Your Own Service Plugin

Want to create your own service plugin? See [CONTRIBUTING.md](CONTRIBUTING.md) for a complete guide.

### Quick Development Setup

1. **Copy a template:**
   ```bash
   cp -r service.seranov.template1 service.seranov.myplugin
   ```

2. **Update metadata:**
   - Edit `addon.xml` with your plugin details
   - Update strings in `resources/language/resource.language.en_gb/strings.xml`

3. **Implement your logic:**
   - Edit `service.py` to add your custom functionality

4. **Test locally:**
   - Copy to Kodi's addons directory
   - Restart Kodi
   - Enable the service

5. **Build repository:**
   ```bash
   python3 scripts/generate_repo.py
   ```

## Troubleshooting

### Service not starting

1. Check if the service is enabled:
   - **Settings** → **Add-ons** → **My Add-ons** → **Services** → Select your service → **Enable**

2. Check the Kodi log for errors:
   - Enable debug logging
   - Look for error messages related to your service

3. Verify dependencies:
   - Ensure all required dependencies are installed

### Service not working as expected

1. Enable debug mode in the service settings
2. Check the Kodi log for detailed messages
3. Verify your settings are correct
4. Test with a simple action to isolate the issue

### Changes not taking effect

1. Disable the service
2. Restart Kodi
3. Enable the service again

## Repository Updates

To update add-ons from the repository:

1. The repository checks for updates automatically
2. Go to **Settings** → **Add-ons** → **My Add-ons**
3. Select an add-on with an available update
4. Click **Update**

Or update all add-ons at once:
- **Settings** → **Add-ons** → **Updates** → **Update all**

## Support

For issues, questions, or contributions:
- GitHub Issues: [https://github.com/seranov/kodi-play-random/issues](https://github.com/seranov/kodi-play-random/issues)
- Email: seranov@yandex.ru

## Links

- [README.md](README.md) - Full documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
- [Kodi Add-on Development](https://kodi.wiki/view/Add-on_development)
