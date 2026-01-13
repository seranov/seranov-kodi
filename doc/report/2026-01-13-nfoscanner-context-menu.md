# NFO Scanner Context Menu Implementation Report

**Date:** 2026-01-13  
**Task:** Add context menu for manual folder scanning in nfoscanner plugin

## Summary

Successfully implemented context menu functionality for the `service.seranov.nfoscanner` addon that allows users to manually trigger NFO scanning for individual folders directly from the Kodi interface.

## Requirements

The task required:
1. Add a context menu item for folders in Kodi
2. The context menu should trigger manual NFO scanning for the selected folder
3. Use the same scanning logic that exists in the service plugin (`scan_folder` method)
4. Show progress and results to the user

## Implementation Details

### Plugin Modified: service.seranov.nfoscanner

**Version:** 1.1.0 → 1.1.1 (patch increment as required)

### Changes Made

#### 1. Created Context Menu Script (`context_menu.py`)
- **Purpose:** Entry point for the context menu action
- **Functionality:**
  - Retrieves the selected folder path from the list item
  - Creates a `NFOScanner` instance
  - Calls the `scan_folder()` method with the selected folder path
  - Shows a progress dialog during scanning
  - Displays notification with scan results
  - Handles errors gracefully with appropriate error messages

**Key Features:**
- Reuses existing `NFOScanner` class and its `scan_folder()` method
- No code duplication - calls the exact same scanning logic as the service
- User-friendly progress indication
- Localized result messages

#### 2. Updated `addon.xml`
- Added `<extension point="kodi.context.item">` section
- Configured to appear in the main Kodi context menu (`kodi.core.main`)
- Set visibility condition to show only on folders using `ListItem.IsFolder`
- Uses localized string for menu label (string ID: 32124)
- Updated version from 1.1.0 to 1.1.1

#### 3. Added Localization Strings

**English (`resource.language.en_gb/strings.xml`):**
- `32120`: "No folder selected"
- `32121`: "Scanning folder..."
- `32122`: "Scanned {0} items"
- `32123`: "No items needed updating"
- `32124`: "Update NFO Info"

**Russian (`resource.language.ru_ru/strings.xml`):**
- `32120`: "Папка не выбрана"
- `32121`: "Сканирование папки..."
- `32122`: "Отсканировано {0} элементов"
- `32123`: "Обновление не требуется"
- `32124`: "Обновить NFO информацию"

### Technical Implementation

#### Context Menu Entry Point

```python
def scan_folder_manually():
    """Scan the selected folder manually"""
    # Get the folder path from sys.listitem
    folder_path = sys.listitem.getPath()
    
    # Create scanner instance
    scanner = NFOScanner(addon, monitor)
    
    # Scan the folder (same code as service uses)
    scanned_count = scanner.scan_folder(folder_path)
    
    # Show result notification
    xbmcgui.Dialog().notification(...)
```

#### Context Menu Configuration in addon.xml

```xml
<extension point="kodi.context.item">
    <menu id="kodi.core.main">
        <item library="context_menu.py">
            <label>$ADDON[service.seranov.nfoscanner 32124]</label>
            <visible>ListItem.IsFolder</visible>
        </item>
    </menu>
</extension>
```

### Scanning Logic

The context menu uses the existing `scan_folder()` method from `NFOScanner` class:
1. Reads `category.nfo` from current folder for genre information
2. Checks for `movie.nfo` in the folder
3. Compares NFO modification time with Kodi database timestamp
4. Re-imports movie if NFO is newer
5. Recursively scans subdirectories
6. Returns count of updated items

This ensures consistency between automatic and manual scanning.

## Validation

### Python Syntax Check
All Python files compiled successfully with `py_compile`:
```bash
python3 -m py_compile service.seranov.nfoscanner/*.py
python3 -m py_compile service.seranov.nfoscanner/resources/lib/*.py
# No errors
```

### XML Validation
All XML files are well-formed:
- `addon.xml` - Valid
- `resources/settings.xml` - Valid
- Language strings files - Valid

## User Experience

### How to Use
1. Navigate to any folder in Kodi's video library
2. Right-click (or press context menu key) on the folder
3. Select "Update NFO Info" (or "Обновить NFO информацию" in Russian)
4. A progress dialog appears showing "Scanning folder..."
5. After completion, a notification shows:
   - "Scanned X items" if updates were made
   - "No items needed updating" if everything was up to date
   - "Error during scan" if something went wrong

### Benefits
- **On-demand scanning:** Users can manually trigger scanning without waiting for the service's scheduled scan
- **Immediate feedback:** Progress dialog and notification inform users of the operation
- **Targeted updates:** Scan only the folder of interest instead of all sources
- **Integrated workflow:** Accessible directly from the context menu where users browse content

## Files Modified

### service.seranov.nfoscanner
- `addon.xml` - Added context menu extension, updated version to 1.1.1
- `context_menu.py` - NEW FILE - Context menu entry point
- `resources/language/resource.language.en_gb/strings.xml` - Added 5 new strings (32120-32124)
- `resources/language/resource.language.ru_ru/strings.xml` - Added 5 new strings (32120-32124)

## Testing Recommendations

While the implementation has been validated for syntax and structure, full functional testing in a live Kodi environment is recommended:

1. **Context Menu Display Test:** 
   - Navigate to various folder types (movies, TV shows, etc.)
   - Verify context menu item appears appropriately
   
2. **Scan Execution Test:**
   - Select "Update NFO Info" from context menu
   - Verify progress dialog appears
   - Confirm scanning completes successfully
   
3. **Result Notification Test:**
   - Test folder with outdated NFO files (should show "Scanned X items")
   - Test folder with up-to-date NFO files (should show "No items needed updating")
   
4. **Error Handling Test:**
   - Test on non-folder items (should handle gracefully)
   - Test on empty/invalid paths
   
5. **Localization Test:**
   - Verify English strings display correctly in English locale
   - Verify Russian strings display correctly in Russian locale
   
6. **Integration Test:**
   - Verify manual scan doesn't interfere with automatic service scanning
   - Confirm database updates are reflected in Kodi library

## Conclusion

All requirements have been successfully implemented:
- ✅ Context menu item added for folders in Kodi
- ✅ Manual NFO scanning functionality implemented
- ✅ Uses existing `scan_folder()` logic from service plugin (no code duplication)
- ✅ Progress indication and result notifications
- ✅ Version incremented (1.1.0 → 1.1.1)
- ✅ Full localization for English and Russian
- ✅ All XML files are valid
- ✅ All Python files have correct syntax
- ✅ Graceful error handling

The implementation is minimal, focused, and follows the existing patterns in the codebase. It provides users with convenient manual control over NFO scanning while maintaining consistency with the automatic scanning service.
