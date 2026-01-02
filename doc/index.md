# Документация / Documentation

Эта папка содержит документацию на русском языке для репозитория аддонов Kodi.

This folder contains Russian language documentation for the Kodi addons repository.

## Файлы документации / Documentation Files

### [README.ru.md](README.ru.md)
Основная документация репозитория на русском языке, включающая:
- Описание структуры репозитория
- Список доступных аддонов и их возможностей
- Инструкции по установке
- Руководство по разработке

Main repository documentation in Russian, including:
- Repository structure description
- List of available addons and their features
- Installation instructions
- Development guide

### [QUICKSTART.ru.md](QUICKSTART.ru.md)
Краткое руководство по быстрому старту:
- Установка репозитория и аддонов
- Использование плагинов-служб
- Настройка и конфигурация
- Устранение неполадок

Quick start guide covering:
- Repository and addon installation
- Using service plugins
- Configuration and settings
- Troubleshooting

### [CONTRIBUTING.ru.md](CONTRIBUTING.ru.md)
Подробное руководство для разработчиков:
- Создание новых плагинов-служб
- Использование шаблонов
- Лучшие практики разработки
- Тестирование и отладка
- Локализация

Detailed guide for developers:
- Creating new service plugins
- Using templates
- Development best practices
- Testing and debugging
- Localization

## Английская документация / English Documentation

Документация на английском языке находится в корне репозитория:

English documentation is located in the repository root:

- [../README.md](../README.md) - Main documentation
- [../QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [../CONTRIBUTING.md](../CONTRIBUTING.md) - Contributing guide

## Дополнительные ресурсы / Additional Resources

### Официальная документация Kodi / Official Kodi Documentation
- [Разработка аддонов для Kodi](https://kodi.wiki/view/Add-on_development)
- [Python API для Kodi](https://codedocs.xyz/xbmc/xbmc/)
- [JSON-RPC API](https://kodi.wiki/view/JSON-RPC_API)

### Структура проекта / Project Structure

```
kodi-play-random/
├── plugin.video.random.recursive/  # Плагин случайного воспроизведения
├── context.screenshots/            # Контекстное меню для скриншотов
├── service.seranov.template1/      # Шаблон службы 1 (периодическая)
├── service.seranov.template2/      # Шаблон службы 2 (управляемая событиями)
├── repository.seranov/             # Репозиторий аддонов
├── repo/                           # Сгенерированные zip-файлы
├── scripts/                        # Скрипты сборки
└── doc/                            # Русская документация
    ├── README.ru.md
    ├── QUICKSTART.ru.md
    ├── CONTRIBUTING.ru.md
    └── index.md (этот файл)
```

## Контакты / Contact

- **GitHub Issues**: [https://github.com/seranov/kodi-play-random/issues](https://github.com/seranov/kodi-play-random/issues)
- **Email**: seranov@yandex.ru

## Лицензия / License

MIT License - См. [LICENSE](../LICENSE) для деталей / See [LICENSE](../LICENSE) for details
