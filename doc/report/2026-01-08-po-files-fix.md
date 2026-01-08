# Исправление ошибок парсинга PO-файлов локализации

**Дата:** 2026-01-08  
**Статус:** Завершено

## Проблема

При загрузке аддонов Kodi выдавал ошибки парсинга PO-файлов:

```
POParser: unable to read PO file header from file: 
  C:\Users\Bidon\AppData\Roaming\Kodi\addons\context.screenshots\resources\language\resource.language.ru_ru\strings.po
POParser: unable to read PO file header from file: 
  C:\Users\Bidon\AppData\Roaming\Kodi\addons\context.screenshots\resources\language\resource.language.en_gb\strings.po
```

## Причина

PO-файлы не содержали обязательного заголовка с метаданными (metadata block), который требуется парсеру Kodi для корректной обработки файлов локализации.

## Выполненные изменения

### 1. context.screenshots

Добавлены полные заголовки PO-файлов для обеих локализаций:

- `context.screenshots/resources/language/resource.language.ru_ru/strings.po`
- `context.screenshots/resources/language/resource.language.en_gb/strings.po`

### 2. plugin.video.random.recursive

Дополнены существующие базовые заголовки полными метаданными:

- `plugin.video.random.recursive/resources/language/resource.language.ru_ru/strings.po`
- `plugin.video.random.recursive/resources/language/resource.language.en_gb/strings.po`

## Структура заголовка

Добавлен стандартный заголовок PO-файла:

```po
msgid ""
msgstr ""
"Project-Id-Version: {addon_id} {version}\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2026-01-08 10:00+0000\n"
"PO-Revision-Date: 2026-01-08 10:00+0000\n"
"Last-Translator: seranov\n"
"Language-Team: {Language}\n"
"Language: {lang_code}\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
```

## Проверка других аддонов

- ✅ `plugin.video.unified.browser` - использует формат XML (strings.xml), исправления не требуется
- ✅ `service.seranov.nfoscanner` - использует формат XML (strings.xml), исправления не требуется

## Результат

После исправления файлы локализации будут корректно парситься Kodi, и ошибки больше не должны появляться.

## Следующие шаги

1. Протестировать загрузку аддонов в Kodi для подтверждения исправления
2. При необходимости обновить версии аддонов и пересобрать ZIP-архивы для репозитория

