# Руководство по сборке и публикации

> [English version / Английская версия](BUILD_AND_PUBLISH.md)

Это руководство объясняет, как собирать и публиковать релизы репозитория Kodi с автоматическим развертыванием на GitHub Pages.

## Обзор

Репозиторий использует автоматизированный CI/CD пайплайн, который:
- ✅ Собирает ZIP-архивы для всех аддонов
- ✅ Генерирует `addons.xml` и `addons.xml.md5`
- ✅ Автоматически развертывает на GitHub Pages
- ✅ Обеспечивает автоматические обновления в Kodi

**URL репозитория:** `https://seranov.github.io/kodi-play-random/`

---

## Локальная сборка (тестирование)

### Требования

- Python 3.9 или новее
- PowerShell (Windows) или Bash (Linux/Mac)
- Git

### Сборка репозитория локально

#### Windows (PowerShell)

```powershell
# Перейти в корень репозитория
cd C:\prj\kodi-play-random

# Запустить скрипт сборки
.\scripts\build-release.ps1
```

**Опции сборки:**

```powershell
# Сборка с указанной версией
.\scripts\build-release.ps1 -Version "1.0.1"

# Пропустить сборку, только показать информацию
.\scripts\build-release.ps1 -SkipBuild

# Создать git tag
.\scripts\build-release.ps1 -CreateGitTag
```

#### Linux/Mac (Bash)

```bash
# Перейти в корень репозитория
cd ~/kodi-play-random

# Запустить Python генератор напрямую
python3 scripts/generate_repo.py
```

### Что будет собрано

После запуска сборки директория `repo/` будет содержать:

```
repo/
├── addons.xml              # Метаданные репозитория
├── addons.xml.md5          # Файл контрольной суммы
├── context.screenshots/
│   ├── context.screenshots-1.0.5.zip
│   └── icon.png
├── plugin.video.random.recursive/
│   ├── plugin.video.random.recursive-1.0.0.zip
│   └── icon.png
├── plugin.video.unified.browser/
│   ├── plugin.video.unified.browser-1.0.0.zip
│   └── icon.png
├── repository.seranov/
│   ├── repository.seranov-1.0.0.zip
│   └── icon.png
└── service.seranov.nfoscanner/
    ├── service.seranov.nfoscanner-1.0.0.zip
    └── icon.png
```

---

## Автоматическое развертывание на GitHub Pages

### Как это работает

Репозиторий использует **GitHub Actions** для автоматической сборки и развертывания при каждом push в `main`:

1. **Триггер:** Push в ветку `main` или тег начинающийся с `v*`
2. **Сборка:** Создаются все ZIP-архивы и файлы метаданных
3. **Развертывание:** Публикация в ветку `gh-pages`
4. **Доступность:** Файлы доступны по адресу `https://seranov.github.io/kodi-play-random/`

### Файл workflow

`.github/workflows/publish-release.yml`

**Ключевые функции:**
- ✅ Python 3.9+ для современных Path API
- ✅ Создание ZIP-архивов для всех аддонов
- ✅ Генерация `addons.xml` с правильным форматированием
- ✅ Расчет MD5 контрольных сумм
- ✅ Развертывание на GitHub Pages (ветка `gh-pages`)
- ✅ Создание `.nojekyll` для отключения обработки Jekyll

### Мониторинг развертываний

1. **Просмотр GitHub Actions:**
   - Перейдите: https://github.com/seranov/kodi-play-random/actions
   - Проверьте статус workflow: **Publish Kodi Repository**

2. **Проверка ветки gh-pages:**
   - Перейдите: https://github.com/seranov/kodi-play-random/tree/gh-pages
   - Убедитесь, что файлы присутствуют

3. **Тест URL репозитория:**
   - Посетите: https://seranov.github.io/kodi-play-random/addons.xml
   - Должен отобразиться XML контент

---

## Публикация нового релиза

### Шаг 1: Обновить номера версий

Обновите версию в соответствующих файлах `addon.xml`:

**Пример:** Обновление `plugin.video.random.recursive/addon.xml`
```xml
<addon id="plugin.video.random.recursive" version="1.0.1" ...>
```

**Файлы для проверки:**
- `plugin.video.random.recursive/addon.xml`
- `plugin.video.unified.browser/addon.xml`
- `context.screenshots/addon.xml`
- `service.seranov.nfoscanner/addon.xml`
- `repository.seranov/addon.xml` (если меняется версия репозитория)

### Шаг 2: Обновить changelog

Добавьте изменения в файлы changelog:
- `doc/RELEASE_NOTES.md`
- Отдельные changelog аддонов (если есть)

### Шаг 3: Commit и Push

```bash
# Добавить изменения
git add .

# Commit с описательным сообщением
git commit -m "Release version 1.0.1

- Обновлен plugin.video.random.recursive до 1.0.1
- Исправлены проблемы с воспроизведением
- Добавлены новые функции"

# Push в main
git push origin main
```

### Шаг 4: Создать Git Tag (опционально)

```bash
# Создать аннотированный тег
git tag -a v1.0.1 -m "Release version 1.0.1"

# Push тега
git push origin v1.0.1
```

### Шаг 5: Дождаться развертывания

1. **GitHub Actions запускается автоматически** после push
2. **Отслеживайте прогресс** на: https://github.com/seranov/kodi-play-random/actions
3. **Развертывание занимает ~1-2 минуты**
4. **Проверьте, что GitHub Pages** обновился

### Шаг 6: Проверить развертывание

```bash
# Проверить, что addons.xml обновлен
curl https://seranov.github.io/kodi-play-random/addons.xml

# Проверить, что ZIP конкретного аддона существует
curl -I https://seranov.github.io/kodi-play-random/plugin.video.random.recursive/plugin.video.random.recursive-1.0.1.zip
```

### Шаг 7: Протестировать в Kodi

1. Откройте Kodi
2. Перейдите в **Дополнения** → **Seranov's Kodi Repository**
3. Правый клик → **Проверить обновления**
4. Убедитесь, что новая версия появилась

---

## Создание GitHub Releases (опционально)

Хотя GitHub Pages обрабатывает автоматические обновления, вы все равно можете создавать GitHub Releases для лучшей видимости:

### Шаг 1: Перейти к Releases

Посетите: https://github.com/seranov/kodi-play-random/releases/new

### Шаг 2: Заполнить форму Release

- **Tag version:** `v1.0.1` (выберите существующий или создайте новый)
- **Target:** `main`
- **Release title:** `v1.0.1 - Обновление функций`
- **Description:** Скопируйте из `RELEASE_NOTES.md`

### Шаг 3: Прикрепить файлы (опционально)

Загрузите ключевые файлы из директории `repo/`:
- `repository.seranov-1.0.0.zip` (основной файл установки)
- Обновленные ZIP аддонов

### Шаг 4: Опубликовать Release

Нажмите **Publish release**

---

## Конфигурация GitHub Pages

### Начальная настройка (уже выполнена)

Репозиторий настроен с:

1. **Настройки GitHub Pages:**
   - Источник: ветка `gh-pages`
   - Пользовательский домен: Нет
   - URL: `https://seranov.github.io/kodi-play-random/`

2. **Настройки репозитория:**
   - Права workflow: Чтение и запись
   - Pages включен

### Проверка конфигурации

1. Перейдите: https://github.com/seranov/kodi-play-random/settings/pages
2. Проверьте:
   - ✅ Источник: Deploy from branch `gh-pages`
   - ✅ Ветка: `gh-pages` / `root`
   - ✅ Статус: **Your site is live at https://seranov.github.io/kodi-play-random/**

---

## Устранение неполадок

### Развертывание не удалось

**Проверьте логи GitHub Actions:**
1. Перейдите: https://github.com/seranov/kodi-play-random/actions
2. Кликните на неудавшийся workflow
3. Просмотрите сообщения об ошибках

**Частые проблемы:**
- Отсутствуют файлы `addon.xml`
- Неверный синтаксис XML
- Несоответствие версии Python (требуется 3.9+)

### GitHub Pages не обновляется

**Решения:**
1. **Проверьте, что ветка gh-pages существует:**
   - https://github.com/seranov/kodi-play-random/tree/gh-pages

2. **Очистите кэш GitHub Pages:**
   - Подождите 5-10 минут для распространения CDN
   - Попробуйте в режиме инкогнито/приватном окне браузера

3. **Проверьте права workflow:**
   - Settings → Actions → General → Workflow permissions
   - Должно быть: **Read and write permissions**

### Kodi не обнаруживает обновления

**Решения:**
1. **Принудительная проверка обновлений:**
   - Правый клик на репозитории → Проверить обновления

2. **Проверьте addons.xml:**
   - Посетите: https://seranov.github.io/kodi-play-random/addons.xml
   - Убедитесь, что номера версий правильные

3. **Проверьте лог Kodi:**
   - Ищите ошибки обновления репозитория
   - Windows: `%APPDATA%\Kodi\kodi.log`

---

## Продвинутое: Ручное развертывание

Если автоматическое развертывание не удалось, вы можете развернуть вручную:

### Шаг 1: Собрать локально

```powershell
# Собрать репозиторий
.\scripts\build-release.ps1
```

### Шаг 2: Скопировать в директорию docs/

```powershell
# Скопировать содержимое repo в docs/
Copy-Item -Path repo\* -Destination docs\ -Recurse -Force
```

### Шаг 3: Commit и Push

```bash
git add docs/
git commit -m "Manual deployment"
git push origin main
```

### Шаг 4: Развернуть в gh-pages

```bash
# Используя subtree push
git subtree push --prefix docs origin gh-pages

# Или принудительный push если нужно
git push origin `git subtree split --prefix docs main`:gh-pages --force
```

---

## Справочник по структуре файлов

### Исходные файлы (в корне репозитория)

```
plugin.video.random.recursive/
  addon.xml              # Версия: 1.0.0
  main.py
  resources/...

context.screenshots/
  addon.xml              # Версия: 1.0.5
  addon.py
  resources/...

repository.seranov/
  addon.xml              # Версия: 1.0.0
  icon.png

scripts/
  build-release.ps1      # Скрипт сборки для Windows
  generate_repo.py       # Python генератор
  deploy-local.ps1       # Локальное развертывание
```

### Сгенерированные файлы (в repo/ и docs/)

```
repo/                    # Локальный вывод сборки
docs/                    # Контент GitHub Pages (развернут в gh-pages)
  addons.xml
  addons.xml.md5
  .nojekyll
  context.screenshots/
    context.screenshots-1.0.5.zip
    icon.png
  plugin.video.random.recursive/
    plugin.video.random.recursive-1.0.0.zip
    icon.png
  ...
```

---

## Лучшие практики

### Нумерация версий

Следуйте Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR:** Ломающие изменения
- **MINOR:** Новые функции, обратная совместимость
- **PATCH:** Исправления ошибок

### Сообщения Commit

Используйте понятные, описательные сообщения commit:

```
✅ Хорошо:
Release version 1.0.1 - Исправлено воспроизведение видео

❌ Плохо:
обновление
исправление
изменения
```

### Тестирование перед релизом

1. **Сначала соберите локально:**
   ```powershell
   .\scripts\build-release.ps1
   ```

2. **Протестируйте установку ZIP в Kodi:**
   - Установите из файлов `repo/*.zip`
   - Проверьте, что аддоны работают правильно

3. **Проверьте метаданные:**
   - Откройте `repo/addons.xml`
   - Проверьте все версии и зависимости

### Документация

Всегда обновляйте:
- ✅ `RELEASE_NOTES.md` - Изменения для пользователей
- ✅ `addon.xml` - Номера версий
- ✅ Разделы Changelog

---

## Ресурсы

### Документация
- [Руководство по установке](INSTALLATION.ru.md)
- [Примечания к релизу](RELEASE_NOTES.md)
- [Руководство по участию](CONTRIBUTING.ru.md)

### Скрипты
- `scripts/build-release.ps1` - Сборка и релиз для Windows
- `scripts/generate_repo.py` - Python генератор репозитория
- `scripts/deploy-local.ps1` - Локальное развертывание в Kodi

### Внешние ссылки
- [Разработка дополнений Kodi](https://kodi.wiki/view/Add-on_development)
- [Документация GitHub Pages](https://docs.github.com/en/pages)
- [Документация GitHub Actions](https://docs.github.com/en/actions)

---

## Поддержка

Если вы столкнулись с проблемами:

1. **Проверьте документацию:** [doc/](../doc/)
2. **GitHub Issues:** [github.com/seranov/kodi-play-random/issues](https://github.com/seranov/kodi-play-random/issues)
3. **Email:** seranov@yandex.ru

---

**Последнее обновление:** 2026-01-07

