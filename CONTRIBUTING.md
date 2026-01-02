# Contributing to Seranov's Kodi Add-ons Repository

Thank you for your interest in contributing! This guide will help you create new service plugins for this repository.

## Creating a New Service Plugin

### Step 1: Use the NFO Scanner as a Reference

The `service.seranov.nfoscanner` addon provides a good example of a complete service plugin with:

- Background scanning with configurable intervals
- Event monitoring (playback, settings changes)
- JSON-RPC API integration with Kodi
- Threading support
- Settings management
- Localization support

You can use it as a reference for creating your own service plugins.

### Step 2: Create Your Service Structure

```bash
# Create the service directory
mkdir -p service.seranov.yourplugin/resources/lib
mkdir -p service.seranov.yourplugin/resources/language/resource.language.en_gb
```

### Step 3: Update addon.xml

Edit `service.seranov.yourplugin/addon.xml`:

1. Change the `id` attribute: `service.seranov.yourplugin`
2. Update the `name` attribute: `Your Plugin Name`
3. Update `version` to `1.0.0`
4. Update `summary` and `description`
5. Keep the `provider-name` as `seranov` or change to your name

Example:
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="service.seranov.myplugin" name="My Custom Service" version="1.0.0" provider-name="seranov">
    <requires>
        <import addon="xbmc.python" version="3.0.0"/>
    </requires>
    <extension point="xbmc.service" library="service.py"/>
    <extension point="xbmc.addon.metadata">
        <summary lang="en_GB">My custom service plugin</summary>
        <description lang="en_GB">This service does something useful</description>
        ...
    </extension>
</addon>
```

### Step 4: Implement Your Service Logic

Edit `service.seranov.yourplugin/service.py`:

**For Template 1 (Periodic Service):**
- Modify the `do_service_work()` method to implement your logic
- Adjust the `check_interval` setting as needed

**For Template 2 (Event-Driven Service):**
- Implement `on_playback_started()` and `on_playback_stopped()` methods
- Add additional event handlers in the `ServiceMonitor` class
- Modify the `run()` method if needed

### Step 5: Update Settings

Edit `service.seranov.yourplugin/resources/settings.xml`:

Add or modify settings for your plugin. Example:

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<settings>
    <category label="32001">
        <setting id="my_setting" type="text" label="32020" default="value"/>
        <setting id="enable_feature" type="bool" label="32021" default="true"/>
    </category>
</settings>
```

### Step 6: Update Language Strings

Edit `service.seranov.yourplugin/resources/language/resource.language.en_gb/strings.xml`:

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<strings>
    <string id="32000">Your Plugin Name</string>
    <string id="32001">General</string>
    <string id="32020">My Setting</string>
    <string id="32021">Enable Feature</string>
</strings>
```

### Step 7: Add Your Icon

Replace the icon if desired:
- File: `service.seranov.yourplugin/icon.png`
- Recommended size: 256x256 pixels or 512x512 pixels
- Format: PNG with transparency

### Step 8: Test Your Plugin Locally

1. Copy your plugin directory to Kodi's addons folder:
   - Linux: `~/.kodi/addons/`
   - Windows: `%APPDATA%\Kodi\addons\`
   - macOS: `~/Library/Application Support/Kodi/addons/`

2. Restart Kodi or refresh add-ons

3. Enable your service in **Settings** → **Add-ons** → **My Add-ons** → **Services**

4. Check the Kodi log for any errors:
   - Linux/macOS: `~/.kodi/temp/kodi.log`
   - Windows: `%APPDATA%\Kodi\kodi.log`

### Step 9: Generate Repository Files

Run the repository generation script:

```bash
python3 scripts/generate_repo.py
```

This will:
- Create a ZIP file for your plugin in the `repo/` directory
- Update `addons.xml` with your plugin's metadata
- Update `addons.xml.md5` checksum

### Step 10: Submit Your Plugin

1. Commit your changes:
   ```bash
   git add service.seranov.yourplugin/
   git commit -m "Add service.seranov.yourplugin"
   ```

2. Push to your branch and create a pull request

## Best Practices

### Code Quality

- Use meaningful variable and function names
- Add comments for complex logic
- Follow PEP 8 style guide for Python code
- Handle exceptions gracefully
- Use logging instead of print statements

### Settings

- Provide sensible default values
- Group related settings in categories
- Use appropriate setting types (text, number, bool, select)
- Add validation for user input

### Logging

Always use the Kodi logging system:

```python
import xbmc

xbmc.log('[service.seranov.yourplugin] Your message', xbmc.LOGINFO)
```

Log levels:
- `xbmc.LOGDEBUG`: Debug messages
- `xbmc.LOGINFO`: Informational messages
- `xbmc.LOGWARNING`: Warnings
- `xbmc.LOGERROR`: Errors
- `xbmc.LOGFATAL`: Fatal errors

### Performance

- Use `monitor.waitForAbort()` for delays instead of `time.sleep()`
- Don't do heavy processing in the main thread
- Respect the `abortRequested()` flag for clean shutdown
- Be mindful of resource usage (CPU, memory, network)

### Localization

- Use string IDs (32000+) for all user-facing text
- Provide English strings at minimum
- Consider adding translations for other languages

## Common Patterns

### Reading Settings

```python
import xbmcaddon

addon = xbmcaddon.Addon()
my_setting = addon.getSetting('my_setting')
enable_feature = addon.getSetting('enable_feature') == 'true'
```

### Showing Notifications

```python
import xbmcgui

xbmcgui.Dialog().notification(
    heading='My Plugin',
    message='Something happened',
    icon=xbmcgui.NOTIFICATION_INFO,
    time=5000  # milliseconds
)
```

### Executing JSON-RPC Commands

```python
import xbmc
import json

request = {
    'jsonrpc': '2.0',
    'method': 'Player.GetActivePlayers',
    'id': 1
}
response = json.loads(xbmc.executeJSONRPC(json.dumps(request)))
```

## Resources

- [Kodi Add-on Development](https://kodi.wiki/view/Add-on_development)
- [Kodi Python API](https://codedocs.xyz/xbmc/xbmc/)
- [Kodi JSON-RPC API](https://kodi.wiki/view/JSON-RPC_API)

## Questions?

If you have questions or need help, please:
1. Check existing service plugins for examples
2. Review the Kodi documentation
3. Open an issue on GitHub

Happy coding! 🎉
