# GitHub Actions Workflow для публикации Kodi-репозитория

[English version below](#github-actions-workflow-for-kodi-repository-publishing)

## Описание

Автоматизированный GitHub Actions workflow для публикации Kodi-репозитория через GitHub Pages.

## Файл

`.github/workflows/publish-release.yml`

## Триггеры

Workflow запускается при:
- **Push в ветку `main`** - автоматическая публикация при каждом коммите
- **Создании тегов `v*`** - публикация релиза при создании тега (например, `v1.0.1`)
- **Ручном запуске** - через интерфейс GitHub Actions (workflow_dispatch)

## Что делает workflow

1. ✅ Клонирует репозиторий
2. ✅ Настраивает Python 3.x
3. ✅ Создаёт структуру директорий `docs/`
4. ✅ Сканирует все директории аддонов (`plugin.*`, `service.*`, `context.*`, `repository.*`)
5. ✅ Извлекает версию из каждого `addon.xml`
6. ✅ Создаёт ZIP-архивы для каждого аддона
7. ✅ Генерирует объединённый `addons.xml`
8. ✅ Создаёт MD5 чексумму (`addons.xml.md5`)
9. ✅ Копирует иконки и фанарты
10. ✅ Создаёт `.nojekyll` файл
11. ✅ Публикует всё в GitHub Pages (ветка `gh-pages`)

## Структура выходных файлов

```
docs/
├── addons.xml                      # Метаданные всех аддонов
├── addons.xml.md5                  # MD5 чексумма
├── .nojekyll                       # Отключение Jekyll
├── context.screenshots/
│   ├── context.screenshots-1.0.5.zip
│   ├── icon.png
│   └── fanart.jpg
├── plugin.video.random.recursive/
│   ├── plugin.video.random.recursive-1.0.0.zip
│   └── icon.png
├── plugin.video.unified.browser/
│   ├── plugin.video.unified.browser-1.0.0.zip
│   └── icon.png
├── service.seranov.nfoscanner/
│   ├── service.seranov.nfoscanner-1.0.0.zip
│   └── icon.png
└── repository.seranov/
    ├── repository.seranov-1.0.0.zip
    └── icon.png
```

## Использование

### Автоматический запуск

Просто сделайте push в ветку `main`:

```bash
git add .
git commit -m "Update addon"
git push origin main
```

Или создайте тег для релиза:

```bash
git tag v1.0.1
git push origin v1.0.1
```

### Ручной запуск

1. Перейдите в **Actions** → **Publish Kodi Repository**
2. Нажмите **Run workflow**
3. Выберите ветку
4. Нажмите **Run workflow**

## Настройка GitHub Pages

После первого запуска workflow:

1. Перейдите в **Settings** → **Pages**
2. В разделе **Source** выберите:
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`
3. Нажмите **Save**

После этого репозиторий будет доступен по адресу:
```
https://seranov.github.io/seranov-kodi/
```

## Установка репозитория в Kodi

1. Скачайте `repository.seranov-1.0.0.zip` из GitHub Pages или Releases
2. В Kodi: **Add-ons** → **Install from zip file**
3. Выберите скачанный ZIP файл
4. Дождитесь уведомления об успешной установке

После установки репозитория все остальные аддоны можно устанавливать через **Install from repository** → **Seranov's Kodi Repository**.

## Логирование

Workflow выводит подробную информацию:
- Список обрабатываемых аддонов
- Версии каждого аддона
- Созданные файлы
- Размеры архивов
- Структуру директории

## Обработка ошибок

- Если `addon.xml` отсутствует - аддон пропускается с предупреждением
- Если XML некорректный - workflow завершается с ошибкой
- Все ошибки выводятся в лог Actions

## Требования

- Python 3.x (устанавливается автоматически)
- Стандартные Linux утилиты: `rsync`, `zip`, `md5sum`
- GitHub Actions права: `contents: write`, `pages: write`, `id-token: write`

## Технические детали

- **Платформа:** `ubuntu-latest`
- **Python:** 3.x
- **Actions:**
  - `actions/checkout@v4`
  - `actions/setup-python@v5`
  - `peaceiris/actions-gh-pages@v4`

## Сравнение с release.bat

| Параметр | release.bat | GitHub Actions |
|----------|-------------|----------------|
| Платформа | ❌ Только Windows | ✅ Любая |
| Запуск | ❌ Ручной | ✅ Автоматический |
| Аддоны | ❌ Один | ✅ Все сразу |
| Публикация | ❌ Ручная | ✅ Автоматическая |
| Зависимости | ❌ 7-Zip | ✅ Встроенные |

---

# GitHub Actions Workflow for Kodi Repository Publishing

## Description

Automated GitHub Actions workflow for publishing a Kodi repository via GitHub Pages.

## File

`.github/workflows/publish-release.yml`

## Triggers

The workflow runs on:
- **Push to `main` branch** - automatic publishing on every commit
- **Tag creation `v*`** - release publishing when creating a tag (e.g., `v1.0.1`)
- **Manual dispatch** - via GitHub Actions interface (workflow_dispatch)

## What the workflow does

1. ✅ Clones the repository
2. ✅ Sets up Python 3.x
3. ✅ Creates `docs/` directory structure
4. ✅ Scans all addon directories (`plugin.*`, `service.*`, `context.*`, `repository.*`)
5. ✅ Extracts version from each `addon.xml`
6. ✅ Creates ZIP archives for each addon
7. ✅ Generates combined `addons.xml`
8. ✅ Creates MD5 checksum (`addons.xml.md5`)
9. ✅ Copies icons and fanarts
10. ✅ Creates `.nojekyll` file
11. ✅ Publishes everything to GitHub Pages (`gh-pages` branch)

## Output file structure

```
docs/
├── addons.xml                      # All addons metadata
├── addons.xml.md5                  # MD5 checksum
├── .nojekyll                       # Disable Jekyll
├── context.screenshots/
│   ├── context.screenshots-1.0.5.zip
│   ├── icon.png
│   └── fanart.jpg
├── plugin.video.random.recursive/
│   ├── plugin.video.random.recursive-1.0.0.zip
│   └── icon.png
├── plugin.video.unified.browser/
│   ├── plugin.video.unified.browser-1.0.0.zip
│   └── icon.png
├── service.seranov.nfoscanner/
│   ├── service.seranov.nfoscanner-1.0.0.zip
│   └── icon.png
└── repository.seranov/
    ├── repository.seranov-1.0.0.zip
    └── icon.png
```

## Usage

### Automatic run

Simply push to the `main` branch:

```bash
git add .
git commit -m "Update addon"
git push origin main
```

Or create a tag for a release:

```bash
git tag v1.0.1
git push origin v1.0.1
```

### Manual run

1. Go to **Actions** → **Publish Kodi Repository**
2. Click **Run workflow**
3. Select branch
4. Click **Run workflow**

## GitHub Pages Setup

After the first workflow run:

1. Go to **Settings** → **Pages**
2. In the **Source** section, select:
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`
3. Click **Save**

After that, the repository will be available at:
```
https://seranov.github.io/seranov-kodi/
```

## Installing the repository in Kodi

1. Download `repository.seranov-1.0.0.zip` from GitHub Pages or Releases
2. In Kodi: **Add-ons** → **Install from zip file**
3. Select the downloaded ZIP file
4. Wait for the success notification

After installing the repository, all other addons can be installed via **Install from repository** → **Seranov's Kodi Repository**.

## Logging

The workflow outputs detailed information:
- List of processed addons
- Version of each addon
- Created files
- Archive sizes
- Directory structure

## Error handling

- If `addon.xml` is missing - addon is skipped with a warning
- If XML is invalid - workflow fails with an error
- All errors are logged in Actions

## Requirements

- Python 3.x (installed automatically)
- Standard Linux utilities: `rsync`, `zip`, `md5sum`
- GitHub Actions permissions: `contents: write`, `pages: write`, `id-token: write`

## Technical details

- **Platform:** `ubuntu-latest`
- **Python:** 3.x
- **Actions:**
  - `actions/checkout@v4`
  - `actions/setup-python@v5`
  - `peaceiris/actions-gh-pages@v4`

## Comparison with release.bat

| Parameter | release.bat | GitHub Actions |
|-----------|-------------|----------------|
| Platform | ❌ Windows only | ✅ Any |
| Run | ❌ Manual | ✅ Automatic |
| Addons | ❌ One | ✅ All at once |
| Publishing | ❌ Manual | ✅ Automatic |
| Dependencies | ❌ 7-Zip | ✅ Built-in |
