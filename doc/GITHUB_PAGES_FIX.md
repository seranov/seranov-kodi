# Исправление проблемы с таймаутом GitHub Pages

## Проблема
Workflow успешно завершает основные шаги, но падает на этапе "pages build and deployment" через 10 минут с ошибкой таймаута.

## Причина
Конфликт между двумя способами деплоя:
1. Старый метод через `peaceiris/actions-gh-pages@v4` (создаёт ветку `gh-pages`)
2. Новый метод через `actions/deploy-pages@v4` (использует артефакты)

## Решение

### 1. Изменения в workflow (уже применены)
- Удалён шаг "Configure GitHub Pages" с curl-запросами
- Удалён `peaceiris/actions-gh-pages@v4`
- Оставлен только новый официальный метод через Actions:
  - `actions/upload-pages-artifact@v3`
  - `actions/deploy-pages@v4`

### 2. Настройка GitHub Pages в репозитории

Перейдите в настройки репозитория на GitHub:

1. **Settings** → **Pages**
2. В разделе **Build and deployment**:
   - **Source**: выберите **GitHub Actions** (не Branch!)
3. Сохраните изменения

### 3. Удаление старой ветки gh-pages (опционально)

Если ранее использовалась ветка `gh-pages`, её можно удалить:

```bash
git push origin --delete gh-pages
```

### 4. Проверка после применения

После коммита и пуша изменений:
1. Workflow должен завершиться успешно
2. Проверьте деплой по адресу: https://seranov.github.io/kodi-play-random/
3. Убедитесь, что файлы доступны:
   - https://seranov.github.io/kodi-play-random/repository.seranov.zip
   - https://seranov.github.io/kodi-play-random/addons.xml
   - https://seranov.github.io/kodi-play-random/index.html

## Преимущества нового метода

- ✅ Не создаёт отдельную ветку gh-pages
- ✅ Быстрее работает
- ✅ Официальная поддержка GitHub
- ✅ Лучше интегрируется с permissions и OIDC
- ✅ Автоматическая очистка старых деплоев

## Дополнительная оптимизация (если всё ещё медленно)

Если деплой всё ещё занимает много времени, можно:

1. **Проверить размер артефактов**:
   ```yaml
   - name: Check artifact size
     run: du -sh docs
   ```

2. **Исключить ненужные файлы**:
   - `.pyc` файлы (уже исключены)
   - `__pycache__` (уже исключены)
   - Большие медиа-файлы (если не нужны)

3. **Использовать сжатие** (артефакты уже сжимаются автоматически)

## Дата исправления
2026-01-13

