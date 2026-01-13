# Plugin Localization Report

**Date:** 2026-01-13  
**Task:** Localize all plugins to Russian and English languages with English as default

## Objective

Ensure all Kodi plugins in the repository are localized to both Russian (ru_RU) and English (en_GB) languages, with English set as the default language.

## Analysis

### Initial Status

Before the changes, the following plugins had localization status:

1. **plugin.video.seranov.browser** ✅
   - English (en_GB): ✅ Present (strings.xml)
   - Russian (ru_RU): ✅ Present (strings.xml)
   - Metadata: ✅ Both languages

2. **plugin.video.seranov.recursive** ✅
   - English (en_GB): ✅ Present (strings.po)
   - Russian (ru_RU): ✅ Present (strings.po)
   - Metadata: ✅ Both languages

3. **service.seranov.nfoscanner** ✅
   - English (en_GB): ✅ Present (strings.xml)
   - Russian (ru_RU): ✅ Present (strings.xml)
   - Metadata: ✅ Both languages

4. **context.seranov.screenshots** ❌
   - English (en_GB): ✅ Present (strings.po)
   - Russian (ru_RU): ❌ Missing
   - Metadata: ❌ Only English in addon.xml

5. **repository.seranov** ✅
   - Metadata: ✅ Both languages in addon.xml

## Changes Made

### 1. Added Russian Localization for context.seranov.screenshots

Created the Russian localization file:
- **File:** `context.seranov.screenshots/resources/language/resource.language.ru_ru/strings.po`
- **Format:** Gettext PO file (matching the English version)
- **Strings translated:** 18 strings covering all UI elements, settings, and context menu items

#### Key Translations:
- `Local Info` → `Локальная информация`
- `Screenshots slide show` → `Слайдшоу скриншотов`
- `Screenshots tile` → `Плитка скриншотов`
- `Startup mode` → `Режим запуска`
- `Use fanart as background if exists` → `Использовать fanart в качестве фона, если доступен`
- `Context Menu` → `Контекстное меню`
- `Show in root menu` → `Показывать в корне меню`
- `Show in SeraNov folder` → `Показывать в папке SeraNov`

### 2. Updated addon.xml Metadata

Updated `context.seranov.screenshots/addon.xml`:
- Fixed language code from `lang="en"` to `lang="en_GB"` for consistency
- Added Russian summary: `Всплывающие скриншоты`
- Added Russian description: `Показывает слайдшоу локальных изображений и опционально содержимое текстового файла file_id.diz`

## Final Status

All plugins now have complete localization:

### Summary Table

| Plugin | English (en_GB) | Russian (ru_RU) | Metadata | Status |
|--------|----------------|-----------------|----------|--------|
| plugin.video.seranov.browser | ✅ | ✅ | ✅ | Complete |
| plugin.video.seranov.recursive | ✅ | ✅ | ✅ | Complete |
| service.seranov.nfoscanner | ✅ | ✅ | ✅ | Complete |
| context.seranov.screenshots | ✅ | ✅ | ✅ | Complete |
| repository.seranov | N/A | N/A | ✅ | Complete |

## Default Language

**English (en_GB) is set as the default language** for all plugins through:

1. **Language folder structure:** All plugins have `resource.language.en_gb` as their primary language folder
2. **Kodi conventions:** The presence of `resource.language.en_gb` folder makes English the default fallback language
3. **Consistent language codes:** All metadata uses `en_GB` and `ru_RU` codes consistently

## File Structure

Each plugin follows this structure:
```
plugin.name/
├── addon.xml (with en_GB and ru_RU metadata)
└── resources/
    └── language/
        ├── resource.language.en_gb/
        │   └── strings.po or strings.xml
        └── resource.language.ru_ru/
            └── strings.po or strings.xml
```

## Technical Details

### File Formats Used

- **PO format** (Gettext):
  - `context.seranov.screenshots`
  - `plugin.video.seranov.recursive`
  
- **XML format**:
  - `plugin.video.seranov.browser`
  - `service.seranov.nfoscanner`

Both formats are supported by Kodi and work correctly for localization.

### Language Codes

- **English:** `en_GB` (British English, Kodi standard)
- **Russian:** `ru_RU` (Russian)

## Testing Recommendations

1. Install the plugins in Kodi with English interface language
2. Verify all strings display in English
3. Switch Kodi to Russian language
4. Verify all strings display in Russian
5. Check context menu items appear in correct language
6. Verify settings dialogs show localized text

## Conclusion

✅ All plugins are now fully localized to both Russian and English languages  
✅ English (en_GB) is set as the default language  
✅ All metadata in addon.xml files includes both language versions  
✅ Consistent language codes used across all plugins  
✅ File structure follows Kodi best practices  

The localization task has been completed successfully. All four plugins plus the repository addon now support both Russian and English languages with English as the default.
