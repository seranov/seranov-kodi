# Release v1.0.0 - Initial Release

## Overview / Обзор

This is the initial release of Seranov's Kodi Add-ons Repository, containing 5 add-ons for Kodi.

Это первый релиз репозитория дополнений Kodi от Seranov, содержащий 5 дополнений для Kodi.

## Installation / Установка

### English

1. Download `repository.seranov-1.0.0.zip` from the releases
2. In Kodi, go to **Add-ons** → **Install from zip file**
3. Browse to the downloaded zip file and install it
4. Go to **Install from repository** → **Seranov's Kodi Repository**
5. Install any add-ons you want

> **Note:** GitHub Raw does not support directory listing. Use direct ZIP installation method above for best results.

### Русский

1. Скачайте `repository.seranov-1.0.0.zip` из релизов
2. В Kodi откройте **Дополнения** → **Установить из файла zip**
3. Найдите скачанный zip-файл и установите его
4. Откройте **Установить из репозитория** → **Seranov's Kodi Repository**
5. Установите нужные дополнения

> **Примечание:** GitHub Raw не поддерживает листинг директорий. Используйте метод прямой установки ZIP-файла выше для лучших результатов.

## Included Add-ons / Включенные дополнения

### 1. Repository Add-on / Репозиторий
**ID:** `repository.seranov` | **Version:** 1.0.0

Install this to get automatic updates for all add-ons in this repository.

Установите это дополнение для автоматического обновления всех дополнений из репозитория.

### 2. Random Recursive Video Player
**ID:** `plugin.video.random.recursive` | **Version:** 1.0.0

Play videos recursively in random order from a directory.

Воспроизведение видео рекурсивно в случайном порядке из директории.

**Features / Возможности:**
- Scans directories recursively for video files / Рекурсивное сканирование директорий для поиска видеофайлов
- Plays videos in random order / Воспроизведение видео в случайном порядке
- Context menu integration / Интеграция в контекстное меню
- Automatic playlist management / Автоматическое управление плейлистами

### 3. Unified Video Browser
**ID:** `plugin.video.unified.browser` | **Version:** 1.0.0

Browse all video content in a unified list without separation by content type.

Просмотр всего видеоконтента в едином списке без разделения по типам.

**Features / Возможности:**
- Shows videos, movies and series in a single interface / Показывает видео, фильмы и сериалы в едином интерфейсе
- Three-view system: Filters, Movie List, and Details / Трехэкранная система: Фильтры, Список фильмов и Детали
- Advanced filtering by year range, genres, tags, and keywords / Расширенная фильтрация по диапазону лет, жанрам, тегам и ключевым словам
- Composite images with overlay icons / Составные изображения с наложенными иконками
- Persistent state (remembers position, filters, and view) / Постоянное состояние (запоминает позицию, фильтры и представление)
- Smart movie detection (folders with video files) / Умное определение фильмов (папки с видеофайлами)
- Default XXX genre/tag exclusion / Исключение XXX жанра/тега по умолчанию
- Image caching for performance / Кэширование изображений для производительности

### 4. Popup Screenshots
**ID:** `context.screenshots` | **Version:** 1.0.5

Display local screenshots and images in a slideshow.

Показ локальных скриншотов и изображений в слайдшоу.

**Features / Возможности:**
- Context menu integration for media items / Интеграция в контекстное меню для медиафайлов
- Slideshow of local images / Слайдшоу локальных изображений
- Support for file_id.diz text files / Поддержка текстовых файлов file_id.diz
- Lightweight and easy to use / Легковесное и простое в использовании

### 5. NFO Scanner Service
**ID:** `service.seranov.nfoscanner` | **Version:** 1.0.0

Background service that scans video folders for movie.nfo and category.nfo files.

Фоновая служба, которая сканирует видеопапки на наличие файлов movie.nfo и category.nfo.

**Features / Возможности:**
- Automatic scanning of video sources for metadata changes / Автоматическое сканирование источников видео на изменения метаданных
- Re-imports movies when movie.nfo is newer than Kodi database / Переимпортирует фильмы, когда movie.nfo новее базы данных Kodi
- Processes category.nfo files for genre management / Обрабатывает файлы category.nfo для управления жанрами
- Pauses during video playback to avoid interference / Приостанавливается во время воспроизведения видео
- Configurable scan intervals and thread count / Настраиваемые интервалы сканирования и количество потоков
- Manual scan controls / Ручное управление сканированием
- Priority scanning based on user folder navigation / Приоритетное сканирование на основе навигации пользователя по папкам
- Supports both local and network sources / Поддержка локальных и сетевых источников

## What's New in This Release / Что нового в этом релизе

- Initial release with 5 fully functional Kodi add-ons / Первый релиз с 5 полностью функциональными дополнениями Kodi
- Bilingual support (English and Russian) for all add-ons / Двуязычная поддержка (английский и русский) для всех дополнений
- Complete documentation in README / Полная документация в README
- Build scripts for easy repository maintenance / Скрипты сборки для простого обслуживания репозитория

## Requirements / Требования

- Kodi 19 Matrix or later / Kodi 19 Matrix или новее
- Python 3.x support / Поддержка Python 3.x

## License / Лицензия

- Repository, Random Recursive Player, Unified Browser, NFO Scanner: MIT License
- Popup Screenshots: GNU GPL v2

## Support / Поддержка

For issues, questions, or contributions, please visit:
Для сообщений об ошибках, вопросов или вклада посетите:

**GitHub:** https://github.com/seranov/kodi-play-random
**Email:** seranov@yandex.ru

---

**Installation Files Included in This Release:**

- `repository.seranov-1.0.0.zip` - Repository add-on (install this first)
- `plugin.video.random.recursive-1.0.0.zip` - Random Recursive Video Player
- `plugin.video.unified.browser-1.0.0.zip` - Unified Video Browser
- `context.screenshots-1.0.5.zip` - Popup Screenshots
- `service.seranov.nfoscanner-1.0.0.zip` - NFO Scanner Service
- `addons.xml` - Repository metadata file
- `addons.xml.md5` - Repository checksum file
