# Руководство по обновлению версий плагинов Kodi

> [English version / Английская версия](VERSION_UPDATE.md)

Это руководство объясняет пошагово, как правильно обновлять версии плагинов Kodi в исходном коде, компилировать их и публиковать таким образом, чтобы Kodi автоматически обнаруживал и устанавливал обновления.

## Содержание

- [Обзор процесса](#обзор-процесса)
- [Предварительные требования](#предварительные-требования)
- [Шаг 1: Обновление версии в исходном коде](#шаг-1-обновление-версии-в-исходном-коде)
- [Шаг 2: Локальное тестирование](#шаг-2-локальное-тестирование)
- [Шаг 3: Публикация изменений](#шаг-3-публикация-изменений)
- [Шаг 4: Автоматическая сборка и развертывание](#шаг-4-автоматическая-сборка-и-развертывание)
- [Шаг 5: Проверка обновления в Kodi](#шаг-5-проверка-обновления-в-kodi)
- [Как работают автоматические обновления](#как-работают-автоматические-обновления)
- [Устранение неполадок](#устранение-неполадок)
- [Примеры](#примеры)

---

## Обзор процесса

Процесс обновления плагина состоит из следующих этапов:

1. **Изменение кода** → Внесение изменений в код плагина
2. **Обновление версии** → Изменение номера версии в `addon.xml`
3. **Локальное тестирование** → Проверка работоспособности локально
4. **Commit и Push** → Отправка изменений в GitHub
5. **Автоматическая сборка** → GitHub Actions создает ZIP-архивы
6. **Автоматическое развертывание** → Публикация на GitHub Pages
7. **Обновление в Kodi** → Kodi автоматически обнаруживает новую версию

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  Изменение  │ --> │  Обновление  │ --> │   Локальное   │
│    кода     │     │   версии     │     │ тестирование  │
└─────────────┘     └──────────────┘     └───────────────┘
                                                  │
                                                  ▼
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│   Kodi      │ <-- │    GitHub    │ <-- │  git push     │
│ обновляет   │     │    Pages     │     │    origin     │
│   плагин    │     │ (автоматом)  │     │     main      │
└─────────────┘     └──────────────┘     └───────────────┘
```

---

## Предварительные требования

### Для разработки

- **Git** - для работы с репозиторием
- **Python 3.9+** - для локального тестирования сборки
- **Текстовый редактор** - VS Code, PyCharm, Sublime Text и т.д.
- **Kodi** - для тестирования плагина

### Для автоматической публикации

- **GitHub Pages** - должен быть включен в настройках репозитория
- **GitHub Actions** - должен быть активирован (включен по умолчанию)
- **Права доступа** - права на запись в репозиторий

### Понимание Semantic Versioning

Версии плагинов следуют формату `MAJOR.MINOR.PATCH`:

- **MAJOR** (1.x.x) - Большие изменения, несовместимые с предыдущими версиями
- **MINOR** (x.1.x) - Новые функции, обратно совместимые
- **PATCH** (x.x.1) - Исправления ошибок, мелкие улучшения

**Примеры:**
- `1.0.0` → `1.0.1` - Исправлена ошибка
- `1.0.1` → `1.1.0` - Добавлена новая функция
- `1.1.0` → `2.0.0` - Изменен API, несовместимо с 1.x

---

## Шаг 1: Обновление версии в исходном коде

### 1.1. Найдите файл addon.xml

Каждый плагин имеет файл `addon.xml` в корневой директории плагина:

```
plugin.video.random.recursive/
├── addon.xml              ← Здесь находится версия
├── main.py
├── icon.png
└── resources/
```

### 1.2. Откройте файл addon.xml

**Пример содержимого:**

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="plugin.video.random.recursive" 
       name="SeraNov Random Recursive Player" 
       version="1.0.0" 
       provider-name="seranov">
    <requires>
        <import addon="xbmc.python" version="3.0.0"/>
    </requires>
    ...
</addon>
```

### 1.3. Измените номер версии

Найдите атрибут `version` в теге `<addon>` и измените его на новый номер версии:

**Было:**
```xml
<addon id="plugin.video.random.recursive" 
       name="SeraNov Random Recursive Player" 
       version="1.0.0" 
       provider-name="seranov">
```

**Стало:**
```xml
<addon id="plugin.video.random.recursive" 
       name="SeraNov Random Recursive Player" 
       version="1.0.1" 
       provider-name="seranov">
```

### 1.4. Обновите changelog (опционально, но рекомендуется)

Если в вашем плагине есть файл `changelog.txt`, добавьте описание изменений:

```
v1.0.1 (2026-01-07)
- Исправлена ошибка воспроизведения видео
- Улучшена обработка путей с кириллицей
- Оптимизирована работа с большими библиотеками

v1.0.0 (2026-01-01)
- Первый релиз
```

### 1.5. Сохраните изменения

Сохраните файл `addon.xml` и все измененные файлы кода плагина.

---

## Шаг 2: Локальное тестирование

### 2.1. Проверьте корректность addon.xml

Убедитесь, что XML файл синтаксически правильный:

```bash
# Linux/Mac
xmllint --noout plugin.video.random.recursive/addon.xml

# Windows (PowerShell)
# Откройте файл в браузере - если откроется без ошибок, значит XML валиден
```

### 2.2. Соберите репозиторий локально (опционально)

Вы можете протестировать процесс сборки локально перед публикацией:

**Windows (PowerShell):**
```powershell
cd C:\prj\seranov-kodi
.\scripts\build-release.ps1
```

**Linux/Mac:**
```bash
cd ~/seranov-kodi
python3 scripts/generate_repo.py
```

Это создаст:
- ZIP-архив плагина в `repo/plugin.video.random.recursive/`
- Обновленный файл `repo/addons.xml`
- Контрольную сумму `repo/addons.xml.md5`

### 2.3. Протестируйте плагин в Kodi

**Вариант 1: Установка из ZIP-архива**

1. Скопируйте сгенерированный ZIP из `repo/plugin.video.random.recursive/plugin.video.random.recursive-1.0.1.zip`
2. В Kodi: **Дополнения** → **Установить из файла ZIP**
3. Выберите скопированный ZIP файл
4. Проверьте работоспособность плагина

**Вариант 2: Прямое развертывание (только Windows)**

```powershell
# Автоматическое копирование в директорию Kodi
.\scripts\deploy-local.ps1 -AddonsToDeploy @('plugin.video.random.recursive')
```

### 2.4. Проверьте функциональность

- Убедитесь, что плагин запускается без ошибок
- Протестируйте все новые функции
- Проверьте, что исправленные ошибки действительно исправлены

---

## Шаг 3: Публикация изменений

### 3.1. Проверьте статус git

```bash
cd /home/runner/work/seranov-kodi/seranov-kodi
git status
```

Вы должны увидеть измененные файлы:
```
modified:   plugin.video.random.recursive/addon.xml
modified:   plugin.video.random.recursive/main.py
```

### 3.2. Добавьте изменения в git

```bash
# Добавить конкретные файлы
git add plugin.video.random.recursive/addon.xml
git add plugin.video.random.recursive/main.py

# Или добавить всю директорию плагина
git add plugin.video.random.recursive/

# Или добавить все измененные файлы
git add .
```

### 3.3. Создайте commit с описательным сообщением

**Хорошее сообщение commit должно:**
- Указывать номер новой версии
- Кратко описывать что изменилось
- Быть на английском языке (рекомендуется для открытых проектов)

**Примеры хороших commit сообщений:**

```bash
# Простое исправление
git commit -m "plugin.video.random.recursive: bump to v1.0.1 - fix video playback"

# Множественные изменения
git commit -m "plugin.video.random.recursive: bump to v1.1.0

- Add support for subtitle auto-loading
- Fix cyrillic paths handling
- Improve performance with large libraries
- Update Russian translations"

# С указанием типа изменений
git commit -m "fix(random.recursive): bump to v1.0.1 - resolve playback issues"
```

### 3.4. Отправьте изменения на GitHub

```bash
git push origin main
```

Если вы работаете в отдельной ветке:
```bash
git push origin feature/version-1.0.1
```

Затем создайте Pull Request в веб-интерфейсе GitHub.

---

## Шаг 4: Автоматическая сборка и развертывание

После того как изменения попадают в ветку `main`, запускается автоматический процесс:

### 4.1. GitHub Actions автоматически запускается

Workflow `.github/workflows/publish-release.yml` активируется автоматически при:
- Push в ветку `main`
- Создании тега вида `v*` (например, `v1.0.1`)
- Ручном запуске через веб-интерфейс

### 4.2. Что делает GitHub Actions

**Шаги автоматической сборки:**

1. **Checkout репозитория** - скачивает код
2. **Установка Python 3.9** - настраивает окружение
3. **Создание структуры директорий** - создает `docs/` и поддиректории
4. **Создание ZIP-архивов** - упаковывает каждый плагин в отдельный ZIP
   ```
   docs/
   └── plugin.video.random.recursive/
       ├── plugin.video.random.recursive-1.0.1.zip
       └── icon.png
   ```
5. **Генерация addons.xml** - создает метаданные репозитория
6. **Генерация addons.xml.md5** - создает контрольную сумму
7. **Создание index.html** - создает веб-страницы для удобного просмотра
8. **Развертывание на GitHub Pages** - публикует в ветку `gh-pages`

### 4.3. Мониторинг процесса

**Отследить статус сборки можно здесь:**

1. Перейдите на страницу Actions: https://github.com/seranov/seranov-kodi/actions
2. Найдите последний workflow run "Publish Kodi Repository"
3. Откройте его и проверьте статус каждого шага

**Статусы workflow:**
- 🟡 **Желтый (In Progress)** - Сборка выполняется
- 🟢 **Зеленый (Success)** - Сборка успешна, плагин опубликован
- 🔴 **Красный (Failed)** - Ошибка сборки, нужно проверить логи

### 4.4. Проверка развертывания

После успешной сборки (обычно 1-3 минуты), проверьте что файлы доступны:

```bash
# Проверка addons.xml
curl https://seranov.github.io/seranov-kodi/addons.xml

# Проверка ZIP архива
curl -I https://seranov.github.io/seranov-kodi/plugin.video.random.recursive/plugin.video.random.recursive-1.0.1.zip
```

Или откройте в браузере:
- https://seranov.github.io/seranov-kodi/
- https://seranov.github.io/seranov-kodi/addons.xml

**Важно:** Обновление на GitHub Pages может занять 5-10 минут из-за кэширования CDN.

---

## Шаг 5: Проверка обновления в Kodi

### 5.1. Автоматическая проверка обновлений

Kodi автоматически проверяет обновления репозиториев:
- Периодически (по умолчанию каждые 24 часа)
- При запуске Kodi
- При ручной проверке

### 5.2. Ручная проверка обновлений

Чтобы сразу увидеть обновление:

1. Откройте Kodi
2. Перейдите в **Дополнения** (Add-ons)
3. Найдите **Seranov's Kodi Repository**
4. Кликните правой кнопкой → **Проверить обновления** (Check for updates)

### 5.3. Установка обновления

Если обновление найдено:

1. Kodi покажет уведомление: "Доступны обновления"
2. Перейдите в **Дополнения** → **Мои дополнения**
3. Найдите плагин с доступным обновлением (помечен иконкой)
4. Кликните → **Обновить** (Update)

Или:
1. **Система** → **Настройки** → **Дополнения**
2. **Обновления** → Включите автоматические обновления
3. Kodi обновит плагины автоматически

### 5.4. Проверка установленной версии

После обновления проверьте версию:

1. **Дополнения** → **Мои дополнения**
2. Выберите плагин
3. Откройте **Информацию** (Information)
4. Проверьте номер версии - должен быть `1.0.1`

---

## Как работают автоматические обновления

### Архитектура системы обновлений

```
┌─────────────────────────────────────────────────────────────┐
│                        GitHub                                │
│  ┌────────────────┐        ┌─────────────────┐              │
│  │  Репозиторий   │ push   │  GitHub Actions │              │
│  │   (main)       │───────>│   Workflow      │              │
│  └────────────────┘        └────────┬────────┘              │
│                                     │                        │
│                                     │ deploy                 │
│                                     ▼                        │
│                            ┌─────────────────┐               │
│                            │  GitHub Pages   │               │
│                            │   (gh-pages)    │               │
│                            └────────┬────────┘               │
└─────────────────────────────────────┼───────────────────────┘
                                      │
                                      │ HTTPS
                                      ▼
                    ┌─────────────────────────────────┐
                    │  https://seranov.github.io/     │
                    │       seranov-kodi/             │
                    │                                 │
                    │  ├── addons.xml                 │
                    │  ├── addons.xml.md5             │
                    │  └── plugin.../plugin....zip    │
                    └────────┬────────────────────────┘
                             │
                             │ проверка каждые 24 часа
                             ▼
                    ┌─────────────────┐
                    │      Kodi       │
                    │  (у пользователя)│
                    └─────────────────┘
```

### Как Kodi узнает об обновлениях

1. **Репозиторий установлен** - У пользователя установлен `repository.seranov`
2. **URL репозитория** - В `repository.seranov/addon.xml` указан URL:
   ```xml
   <datadir>https://seranov.github.io/seranov-kodi/</datadir>
   ```
3. **Периодическая проверка** - Kodi периодически:
   - Скачивает `addons.xml` с указанного URL
   - Сравнивает версии в `addons.xml` с установленными версиями
   - Если версия в `addons.xml` выше - обновление доступно
4. **Уведомление** - Kodi показывает уведомление об обновлении
5. **Установка** - При согласии пользователя Kodi:
   - Скачивает ZIP-архив плагина с GitHub Pages
   - Распаковывает его в свою директорию плагинов
   - Перезагружает плагин

### Файлы отвечающие за обновления

**repository.seranov/addon.xml:**
```xml
<extension point="xbmc.addon.repository" name="Seranov's Kodi Repository">
    <info compressed="false">https://seranov.github.io/seranov-kodi/addons.xml</info>
    <checksum>https://seranov.github.io/seranov-kodi/addons.xml.md5</checksum>
    <datadir zip="true">https://seranov.github.io/seranov-kodi/</datadir>
</extension>
```

- **info** - URL файла с метаданными всех плагинов
- **checksum** - URL контрольной суммы для проверки целостности
- **datadir** - Базовый URL для скачивания ZIP-архивов

**addons.xml:**
```xml
<addons>
    <addon id="plugin.video.seranov.recursive" version="1.0.1" ...>
        ...
    </addon>
    <addon id="context.seranov.screenshots" version="1.0.5" ...>
        ...
    </addon>
    ...
</addons>
```

Этот файл содержит актуальные версии всех плагинов. Kodi сравнивает версии из этого файла с установленными локально.

---

## Устранение неполадок

### Проблема: GitHub Actions не запускается

**Проверьте:**
1. GitHub Actions включен: Settings → Actions → General → Allow all actions
2. Workflow файл существует: `.github/workflows/publish-release.yml`
3. Push был в ветку `main` (не в другую ветку)

**Решение:**
```bash
# Ручной запуск workflow
# Перейдите: https://github.com/seranov/seranov-kodi/actions
# Выберите "Publish Kodi Repository" → Run workflow
```

### Проблема: Сборка завершилась с ошибкой

**Частые причины:**
- Синтаксическая ошибка в `addon.xml`
- Отсутствует обязательный файл (icon.png, addon.xml)
- Неправильный формат версии (должно быть X.Y.Z)

**Решение:**
1. Откройте логи GitHub Actions
2. Найдите строку с ошибкой (обычно красным цветом)
3. Исправьте ошибку
4. Сделайте новый commit и push

**Проверка XML локально:**
```bash
xmllint --noout plugin.video.random.recursive/addon.xml
```

### Проблема: GitHub Pages не обновляется

**Возможные причины:**
1. CDN кэширование (обычно проходит за 5-10 минут)
2. Ветка gh-pages не существует или пуста
3. GitHub Pages не настроен

**Проверка:**
```bash
# Проверьте ветку gh-pages
git ls-remote origin gh-pages

# Проверьте содержимое
# https://github.com/seranov/seranov-kodi/tree/gh-pages
```

**Решение:**
1. Подождите 10 минут для обновления CDN
2. Проверьте Settings → Pages → Source = gh-pages branch
3. Попробуйте в режиме инкогнито браузера (обход локального кэша)

### Проблема: Kodi не видит обновление

**Причины:**
1. GitHub Pages еще не обновился (подождите 10 минут)
2. Kodi еще не проверял обновления
3. Версия в Kodi уже выше или равна

**Решение:**
1. Проверьте что `addons.xml` содержит новую версию:
   ```bash
   curl https://seranov.github.io/seranov-kodi/addons.xml | grep plugin.video.random.recursive
   ```
2. Принудительно проверьте обновления в Kodi:
   - Правый клик на репозитории → Check for updates
3. Проверьте установленную версию:
   - Мои дополнения → Плагин → Информация

### Проблема: Ошибка при установке обновления в Kodi

**Причины:**
1. ZIP файл поврежден или недоступен
2. Недостаточно прав для записи
3. Конфликт зависимостей

**Решение:**
1. Проверьте доступность ZIP:
   ```bash
   curl -I https://seranov.github.io/seranov-kodi/plugin.video.random.recursive/plugin.video.random.recursive-1.0.1.zip
   ```
2. Посмотрите лог Kodi:
   - Windows: `%APPDATA%\Kodi\kodi.log`
   - Linux: `~/.kodi/temp/kodi.log`
   - Mac: `~/Library/Logs/kodi.log`
3. Попробуйте переустановить плагин:
   - Удалите текущую версию
   - Установите новую версию из ZIP вручную

---

## Примеры

### Пример 1: Исправление ошибки (patch версия)

**Сценарий:** Обнаружена ошибка при воспроизведении видео с кириллическими путями

**Шаги:**

1. Исправьте код в `main.py`:
```python
# Было
video_path = path

# Стало
video_path = path.encode('utf-8').decode('utf-8')
```

2. Обновите версию `1.0.0` → `1.0.1` в `addon.xml`:
```xml
<addon id="plugin.video.random.recursive" version="1.0.1" ...>
```

3. Commit и push:
```bash
git add plugin.video.random.recursive/
git commit -m "plugin.video.random.recursive: bump to v1.0.1 - fix cyrillic paths"
git push origin main
```

4. Ждем ~2 минуты пока GitHub Actions отработает
5. Проверяем в Kodi через 10 минут

### Пример 2: Добавление новой функции (minor версия)

**Сценарий:** Добавлена поддержка автоматической загрузки субтитров

**Шаги:**

1. Добавьте новый код в `main.py`:
```python
def load_subtitles(video_path):
    # Новая функция
    subtitle_path = video_path.rsplit('.', 1)[0] + '.srt'
    if os.path.exists(subtitle_path):
        return subtitle_path
    return None
```

2. Обновите версию `1.0.1` → `1.1.0` в `addon.xml`:
```xml
<addon id="plugin.video.random.recursive" version="1.1.0" ...>
```

3. Обновите changelog.txt:
```
v1.1.0 (2026-01-10)
+ Добавлена автоматическая загрузка субтитров
- Исправлена ошибка с кириллическими путями (из v1.0.1)

v1.0.1 (2026-01-07)
- Исправлена ошибка с кириллическими путями

v1.0.0 (2026-01-01)
- Первый релиз
```

4. Commit и push:
```bash
git add plugin.video.random.recursive/
git commit -m "plugin.video.random.recursive: bump to v1.1.0

- Add automatic subtitle loading support
- Subtitles are auto-loaded if .srt file exists
- Updated documentation"
git push origin main
```

### Пример 3: Обновление нескольких плагинов одновременно

**Сценарий:** Обновить два плагина в одном релизе

**Шаги:**

1. Обновите первый плагин:
```bash
# Измените plugin.video.random.recursive/addon.xml
version="1.1.0"
```

2. Обновите второй плагин:
```bash
# Измените context.seranov.screenshots/addon.xml
version="1.0.6"
```

3. Commit и push:
```bash
git add plugin.video.seranov.recursive/ context.seranov.screenshots/
git commit -m "Release multiple addons

- plugin.video.seranov.recursive: v1.1.0 - Add subtitle support
- context.seranov.screenshots: v1.0.6 - Fix image loading issue"
git push origin main
```

4. GitHub Actions соберет оба плагина в одном запуске

### Пример 4: Создание Git тега для релиза (опционально)

**Сценарий:** Создать тег для важного релиза

**Шаги:**

1. После обновления версии и push в main:
```bash
git checkout main
git pull origin main
```

2. Создайте аннотированный тег:
```bash
git tag -a v1.1.0 -m "Release v1.1.0

Major changes:
- plugin.video.seranov.recursive v1.1.0: Subtitle support
- context.seranov.screenshots v1.0.6: Image loading fix
- Updated documentation"
```

3. Отправьте тег на GitHub:
```bash
git push origin v1.1.0
```

4. Создайте GitHub Release (опционально):
   - Перейдите: https://github.com/seranov/seranov-kodi/releases/new
   - Выберите тег: `v1.1.0`
   - Заполните описание
   - Прикрепите ZIP файлы (опционально)
   - Нажмите "Publish release"

---

## Дополнительные ресурсы

### Внутренняя документация
- [BUILD_AND_PUBLISH.ru.md](BUILD_AND_PUBLISH.ru.md) - Подробное руководство по сборке
- [CONTRIBUTING.ru.md](CONTRIBUTING.ru.md) - Руководство по разработке
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - Примечания к релизам
- [README.ru.md](README.ru.md) - Главная страница (русская версия)

### Внешние ссылки
- [Kodi Add-on Development](https://kodi.wiki/view/Add-on_development) - Официальная документация Kodi
- [Semantic Versioning](https://semver.org/lang/ru/) - Стандарт версионирования
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - Документация GitHub Actions
- [GitHub Pages Documentation](https://docs.github.com/en/pages) - Документация GitHub Pages

### Скрипты в репозитории
- `scripts/generate_repo.py` - Python скрипт для генерации репозитория
- `scripts/build-release.ps1` - PowerShell скрипт для сборки (Windows)
- `scripts/deploy-local.ps1` - PowerShell скрипт для локального развертывания
- `.github/workflows/publish-release.yml` - GitHub Actions workflow

---

## Поддержка

Если у вас возникли вопросы или проблемы:

1. **Проверьте документацию:** [doc/](../doc/)
2. **GitHub Issues:** [github.com/seranov/seranov-kodi/issues](https://github.com/seranov/seranov-kodi/issues)
3. **Email:** seranov@yandex.ru

---

**Последнее обновление:** 2026-01-07
