# Context Menu Implementation Report

**Date:** 2026-01-13  
**Task:** Add context menus to all plugins with configurable location settings

## Summary

Successfully implemented context menu functionality for all plugins in the seranov-kodi repository with user-configurable menu location options.

## Requirements

The task required:
1. All plugins must have context menus
2. Settings in all plugins must allow choosing the location of context menu items:
   - Root menu (kodi.core.main)
   - SeraNov subfolder (custom menu id: "seranov")
   - Both locations simultaneously

## Implementation Details

### Plugins Modified

#### 1. plugin.video.seranov.browser
**Status:** Added new context menu functionality

**Changes:**
- Created `context_menu.py` - Entry point for context menu that opens the Unified Browser
- Added context menu extensions to `addon.xml` with two menu locations:
  - Root menu (id: `kodi.core.main`)
  - SeraNov submenu (id: `seranov`)
- Added localized strings for both English and Russian:
  - `32500`: "Open Unified Browser" / "Открыть Unified Browser"
  - `32600`: "Context Menu" / "Контекстное меню"
  - `32601`: "Show in root menu" / "Показывать в корне меню"
  - `32602`: "Show in SeraNov folder" / "Показывать в папке SeraNov"
- Added settings category with two boolean options:
  - `context_menu_root` (default: true)
  - `context_menu_seranov` (default: false)

#### 2. plugin.video.seranov.recursive
**Status:** Enhanced existing context menu with location options

**Changes:**
- Modified existing context menu in `addon.xml` to support dual locations
- Added localized strings for both English and Russian:
  - `32100`: "Context Menu" / "Контекстное меню"
  - `32101`: "Show in root menu" / "Показывать в корне меню"
  - `32102`: "Show in SeraNov folder" / "Показывать в папке SeraNov"
- Added settings category with two boolean options:
  - `context_menu_root` (default: true)
  - `context_menu_seranov` (default: false)
- Updated visibility conditions to use `System.AddonSettings()` checks

#### 3. context.seranov.screenshots
**Status:** Enhanced existing context menu with location options

**Changes:**
- Modified existing context menu in `addon.xml` to support dual locations
- Added localized strings in English:
  - `30200`: "Context Menu"
  - `30201`: "Show in root menu"
  - `30202`: "Show in SeraNov folder"
- Added settings category (version 1 format) with two boolean options:
  - `context_menu_root` (default: true)
  - `context_menu_seranov` (default: false)
- Updated visibility conditions to use `System.AddonSettings()` checks

### Technical Implementation

#### Context Menu Configuration

Each plugin now has two `<extension point="kodi.context.item">` blocks:

**Root Menu:**
```xml
<extension point="kodi.context.item">
    <menu id="kodi.core.main">
        <item library="[script].py">
            <label>$ADDON[addon.id stringid]</label>
            <visible>String.IsEqual(System.AddonSettings(addon.id,context_menu_root),true)</visible>
        </item>
    </menu>
</extension>
```

**SeraNov Submenu:**
```xml
<extension point="kodi.context.item">
    <menu id="seranov">
        <item library="[script].py">
            <label>$ADDON[addon.id stringid]</label>
            <visible>String.IsEqual(System.AddonSettings(addon.id,context_menu_seranov),true)</visible>
        </item>
    </menu>
</extension>
```

The visibility conditions check the user's settings using `System.AddonSettings()` to determine which menu locations should display the context menu item.

#### Settings Format

- `plugin.video.seranov.browser` and `plugin.video.seranov.recursive` use the legacy settings format
- `context.seranov.screenshots` uses the new settings format (version 1)

Both formats support the boolean toggle settings required for this feature.

## Validation

### XML Validation
All XML files (addon.xml and settings.xml) were validated for well-formedness using Python's `xml.etree.ElementTree`. All files passed validation.

### Python Syntax Check
The new `context_menu.py` script was validated for correct Python syntax using `py_compile`. No syntax errors were found.

### Repository Build
Successfully built the repository using `scripts/generate_repo.py`:
- Generated ZIP files for all 5 addons
- Generated `addons.xml` with all context menu definitions
- Generated `addons.xml.md5` checksum
- No build errors or warnings

### Verification
Confirmed that generated `addons.xml` contains:
- Dual context menu extensions for all three plugins
- Correct visibility conditions based on settings
- Proper menu IDs (kodi.core.main and seranov)

## User Experience

### Default Behavior
By default, all plugins show context menu items in the root menu only (`context_menu_root=true`, `context_menu_seranov=false`).

### Configurable Options
Users can configure each plugin independently through its settings:
1. **Root menu only** (default)
2. **SeraNov folder only**
3. **Both locations**
4. **Neither location** (effectively disables context menu)

### Settings Location
Users can access settings via:
- Kodi Add-ons → My Add-ons → [Category] → [Plugin] → Configure
- Context menu on plugin in add-ons list → Settings

## Files Modified

### plugin.video.seranov.browser
- `addon.xml` - Added 2 context menu extensions
- `context_menu.py` - NEW FILE - Context menu entry point
- `resources/settings.xml` - Added context menu settings category
- `resources/language/resource.language.en_gb/strings.xml` - Added 4 new strings
- `resources/language/resource.language.ru_ru/strings.xml` - Added 4 new strings

### plugin.video.seranov.recursive
- `addon.xml` - Modified context menu to add second location
- `resources/settings.xml` - Added context menu settings category
- `resources/language/resource.language.en_gb/strings.po` - Added 3 new strings
- `resources/language/resource.language.ru_ru/strings.po` - Added 3 new strings

### context.seranov.screenshots
- `addon.xml` - Modified context menu to add second location
- `resources/settings.xml` - Added context menu settings category
- `resources/language/resource.language.en_gb/strings.po` - Added 3 new strings

## Testing Recommendations

While this implementation has been validated for syntax and structure, full functional testing in a live Kodi environment is recommended:

1. **Installation Test:** Install all three plugins and verify they appear in appropriate categories
2. **Context Menu Display:** Right-click on video items and verify context menu items appear
3. **Settings Test:** Change settings for each plugin and verify menu items appear/disappear accordingly
4. **Submenu Test:** Enable SeraNov folder option and verify custom submenu appears
5. **Both Locations Test:** Enable both options and verify items appear in both locations
6. **Disable Test:** Disable both options and verify context menu items are hidden

## Conclusion

All requirements have been successfully implemented:
- ✅ All plugins now have context menus
- ✅ All plugins have settings to configure menu location
- ✅ Support for root menu placement
- ✅ Support for SeraNov subfolder placement
- ✅ Support for both locations simultaneously
- ✅ All XML files are valid
- ✅ Repository builds successfully
- ✅ Localization provided for English and Russian

The implementation follows Kodi best practices and maintains consistency across all plugins in the repository.
