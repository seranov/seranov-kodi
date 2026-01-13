# GitHub Pages Timeout - Исправление

## Дата: 2026-01-13

## Проблема
- Workflow успешно проходит основную сборку
- Падает на этапе "pages build and deployment" через 10 минут по таймауту
- Ошибка: `Timeout reached, aborting!`

## Причина
Конфликт между двумя методами деплоя GitHub Pages:
1. ❌ Старый: `peaceiris/actions-gh-pages@v4` → создаёт ветку `gh-pages`
2. ✅ Новый: `actions/deploy-pages@v4` → использует артефакты

## Выполненные изменения

### 1. Файл: `.github/workflows/publish-release.yml`

**Удалено:**
- Шаг "Configure GitHub Pages" с curl-запросами к API
- Action `peaceiris/actions-gh-pages@v4`
- Настройки для ветки `gh-pages`

**Оставлено:**
- `actions/upload-pages-artifact@v3` - загрузка артефакта
- `actions/deploy-pages@v4` - деплой через GitHub Actions
- Правильные permissions в начале workflow

**Исправлено:**
- URL репозитория в финальном сообщении
- Добавлен `deployment.outputs.page_url` для отслеживания

### 2. Создана документация
- `doc/GITHUB_PAGES_FIX.md` - подробное описание проблемы и решения

## Следующие шаги

### Обязательно:
1. **Запушить изменения:**
   ```bash
   git push origin main
   ```

2. **Настроить GitHub Pages:**
   - Перейти: Settings → Pages
   - Source: выбрать **GitHub Actions** (не Branch!)
   - Сохранить

### Опционально:
3. **Удалить старую ветку gh-pages** (если существует):
   ```bash
   git push origin --delete gh-pages
   ```

## Ожидаемый результат
- ✅ Workflow завершается без таймаута
- ✅ Деплой происходит за 1-3 минуты
- ✅ Сайт доступен: https://seranov.github.io/kodi-play-random/
- ✅ Файл репозитория: https://seranov.github.io/kodi-play-random/repository.seranov.zip

## Коммит
```
fix: устранён конфликт деплоя GitHub Pages, используется только новый метод через Actions
```

## Проверка
После пуша проверить:
1. GitHub Actions успешно завершился
2. Страница доступна по URL
3. Файлы корректно деплоятся

