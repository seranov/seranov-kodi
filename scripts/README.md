# Скрипты для разработки и публикации / Development and Publishing Scripts

Эта директория содержит скрипты для локальной разработки, сборки и публикации аддонов Kodi.

This directory contains scripts for local development, building, and publishing Kodi addons.

## Скрипты / Scripts

### 1. `generate_repo.py` - Генерация репозитория
Python-скрипт для создания репозитория Kodi.

**Использование / Usage:**
```bash
python scripts/generate_repo.py
```

**Что делает / What it does:**
- Находит все аддоны (plugin.*, service.*, context.*, repository.*)
- Создает ZIP-файлы для каждого аддона в папке `repo/`
- Генерирует `addons.xml` со всеми метаданными
- Создает контрольную сумму `addons.xml.md5`

### 2. `deploy-local.ps1` - Локальное развертывание
PowerShell-скрипт для копирования аддонов в локальную установку Kodi.

**Использование / Usage:**
```powershell
# Развернуть все аддоны с путями по умолчанию
.\scripts\deploy-local.ps1

# Развернуть конкретные аддоны
.\scripts\deploy-local.ps1 -AddonsToDeploy @('plugin.video.random.recursive', 'context.screenshots')

# Использовать пользовательские пути Kodi
.\scripts\deploy-local.ps1 -KodiDataPath "D:\Kodi\portable_data"

# Полная настройка
.\scripts\deploy-local.ps1 `
    -KodiProgramPath "C:\Program Files\Kodi" `
    -KodiDataPath "$env:APPDATA\Kodi" `
    -AddonsToDeploy @('plugin.video.random.recursive')
```

**Параметры / Parameters:**
- `KodiProgramPath` - Путь к программным файлам Kodi (по умолчанию: `C:\Program Files (x86)\Kodi`)
- `KodiDataPath` - Путь к данным Kodi (по умолчанию: `%APPDATA%\Kodi` или `C:\Users\%USERNAME%\AppData\Roaming\Kodi`)
- `AddonsToDeploy` - Массив имен аддонов для развертывания (пустой = все аддоны)

**Что делает / What it does:**
- Копирует директории аддонов в `%APPDATA%\Kodi\addons\`
- Удаляет старые версии перед копированием
- Показывает статус каждого аддона

**После развертывания / After deployment:**
Перезапустите Kodi для применения изменений.

### 3. `build-release.ps1` - Сборка релиза
PowerShell-скрипт для сборки релиза и подготовки к публикации на GitHub.

**Использование / Usage:**
```powershell
# Собрать репозиторий
.\scripts\build-release.ps1

# Собрать с явной версией
.\scripts\build-release.ps1 -Version "1.0.0"

# Создать git tag
.\scripts\build-release.ps1 -CreateGitTag

# Пропустить сборку (только показать инструкции)
.\scripts\build-release.ps1 -SkipBuild
```

**Параметры / Parameters:**
- `Version` - Версия релиза (автоопределяется из addon.xml, если не указана)
- `SkipBuild` - Пропустить этап сборки
- `CreateGitTag` - Создать git tag для версии
- `GitHubRepo` - Репозиторий GitHub (по умолчанию: `seranov/kodi-play-random`)

**Что делает / What it does:**
- Запускает `generate_repo.py` для сборки всех аддонов
- Проверяет наличие необходимых файлов
- Показывает содержимое репозитория
- Предоставляет инструкции по публикации на GitHub

## Рабочий процесс разработки / Development Workflow

### Локальная разработка / Local Development

1. **Внесите изменения в аддон**
   ```bash
   # Редактируйте файлы в plugin.video.random.recursive/ или другом аддоне
   ```

2. **Разверните в Kodi для тестирования**
   ```powershell
   .\scripts\deploy-local.ps1 -AddonsToDeploy @('plugin.video.random.recursive')
   ```

3. **Перезапустите Kodi и тестируйте**

4. **Повторяйте до готовности**

### Подготовка релиза / Release Preparation

1. **Обновите версию в addon.xml**
   ```xml
   <addon id="plugin.video.random.recursive" version="1.0.1" ...>
   ```

2. **Соберите репозиторий**
   ```powershell
   .\scripts\build-release.ps1
   ```

3. **Проверьте сгенерированные файлы**
   ```bash
   ls repo/
   ```

### Публикация на GitHub / Publishing to GitHub

1. **Зафиксируйте изменения**
   ```bash
   git add .
   git commit -m "Release version 1.0.1"
   ```

2. **Создайте тег (опционально)**
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1"
   ```

3. **Отправьте на GitHub**
   ```bash
   git push origin main
   git push origin v1.0.1  # если создали тег
   ```

4. **Создайте GitHub Release (опционально)**
   - Перейдите на https://github.com/seranov/kodi-play-random/releases/new
   - Выберите тег: `v1.0.1`
   - Название релиза: `Release 1.0.1`
   - Загрузите: `repo/repository.seranov-1.0.0.zip`

## Установка репозитория в Kodi / Installing Repository in Kodi

### Способ 1: Прямая установка из ZIP / Method 1: Direct ZIP Installation

1. **Скачайте ZIP репозитория**
   ```
   https://github.com/seranov/kodi-play-random/raw/main/repo/repository.seranov-1.0.0.zip
   ```

2. **Установите в Kodi:**
   - Откройте Kodi
   - Перейдите: **Настройки** → **Дополнения**
   - Нажмите: **Установить из файла zip**
   - Выберите скачанный файл: `repository.seranov-1.0.0.zip`
   - Дождитесь уведомления "Дополнение установлено"

3. **Установите аддоны из репозитория:**
   - **Настройки** → **Дополнения** → **Установить из репозитория**
   - Выберите **Seranov's Kodi Repository**
   - Выберите категорию и аддон для установки

### Способ 2: Добавление источника репозитория / Method 2: Add Repository Source

Этот способ позволяет Kodi автоматически обновлять аддоны.

1. **Добавьте источник файлов:**
   - **Настройки** → **Диспетчер файлов** → **Добавить источник**
   - Введите URL: `https://raw.githubusercontent.com/seranov/kodi-play-random/main/repo/`
   - Имя: `Seranov Repository`
   - Нажмите **OK**

2. **Установите репозиторий:**
   - **Настройки** → **Дополнения** → **Установить из файла zip**
   - Выберите: **Seranov Repository**
   - Выберите файл: `repository.seranov-1.0.0.zip`

3. **Установите аддоны:**
   - **Настройки** → **Дополнения** → **Установить из репозитория**
   - Выберите **Seranov's Kodi Repository**

### Способ 3: Для разработчиков (прямое копирование) / Method 3: For Developers (Direct Copy)

```powershell
# Используйте скрипт deploy-local.ps1
.\scripts\deploy-local.ps1
```

## URL репозитория / Repository URLs

После публикации на GitHub, пользователи могут использовать эти URL:

**Прямая ссылка на ZIP репозитория:**
```
https://github.com/seranov/kodi-play-random/raw/main/repo/repository.seranov-1.0.0.zip
```

**URL источника репозитория (для автообновлений):**
```
https://raw.githubusercontent.com/seranov/kodi-play-random/main/repo/
```

**Файл metadata репозитория:**
```
https://raw.githubusercontent.com/seranov/kodi-play-random/main/repo/addons.xml
```

## Автоматизация / Automation

### GitHub Actions (опционально)

Вы можете настроить GitHub Actions для автоматической сборки:

```yaml
# .github/workflows/build.yml
name: Build Repository
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: python scripts/generate_repo.py
      - uses: actions/upload-artifact@v2
        with:
          name: repository
          path: repo/
```

## Устранение неполадок / Troubleshooting

### Ошибка: Python не найден
**Решение:** Установите Python 3.x с https://www.python.org/

### Ошибка: PowerShell не может запустить скрипт
**Решение:** Разрешите выполнение скриптов:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Ошибка: Kodi не видит аддоны
**Решение:** 
1. Убедитесь, что пути правильные
2. Перезапустите Kodi
3. Проверьте лог Kodi на наличие ошибок

### Ошибка: Не удается найти addon.xml
**Решение:** Убедитесь, что вы запускаете скрипты из корня репозитория

## Дополнительные ресурсы / Additional Resources

- [Документация Kodi по разработке аддонов](https://kodi.wiki/view/Add-on_development)
- [Формат addon.xml](https://kodi.wiki/view/Addon.xml)
- [Создание репозитория Kodi](https://kodi.wiki/view/HOW-TO:Create_Kodi_add-on_repository)
