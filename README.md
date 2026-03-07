markdown
# ICS → Google Calendar Sync

Утилита для автоматической синхронизации расписания с сайта вуза (в формате ICS) с Google Calendar.

## Возможности
- Загружает актуальный `.ics` с сайта.
- Парсит только ближайшую неделю (`now → now + 7 дней`).
- Сравнивает с предыдущим снимком.
- Синхронизирует календарь:
  - режим **full** — удаляет все события недели и заливает заново;
  - режим **diff** — проверяет изменения, при необходимости перезаливает неделю.
## Установка
1. Клонировать:

   ```bash
   git clone https://github.com/yourname/ics-sync.git
   cd ics-sync
   ```

3. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Получить `credentials.json` в [Google Cloud Console](https://console.cloud.google.com/)
   (тип приложения — **Desktop App**, включён Calendar API).
   Сохранить в `src/data/credentials.json`.

5. На первом запуске откроется окно браузера для авторизации. После неё создастся `src/data/token.json`.

## Использование

После установки как пакета (см. ниже) появится команда `icsync`:

```bash
icsync full    # пересобрать неделю
icsync diff    # проверить изменения и при необходимости обновить
```

### Запуск без упаковки

Можно вызвать напрямую:

```bash
python -m src.app.main full
python -m src.app.main diff
```

## Упаковка в утилиту

В `setup.py` описан entry point:

```python
entry_points={
    "console_scripts": [
        "icsync=src.app.main:main",
    ],
}
```

Установи в editable-режиме:

```bash
pip install -e .
```

Теперь доступна команда:

```bash
icsync full
```

## Автоматизация через cron

Открой редактор:

```bash
crontab -e
```

Добавь правила:

```cron
# каждый день в 07:10 — проверка изменений
10 7 * * * icsync diff >> /home/artem/dev/ics/IcsScriptPG/var/logs/cron.log 2>&1

# каждое воскресенье в 21:00 — пересборка недели
0 21 * * 0 icsync full >> /home/artem/dev/ics/IcsScriptPG/var/logs/cron.log 2>&1
```
