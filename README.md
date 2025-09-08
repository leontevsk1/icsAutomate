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

## Структура проекта


.
├── requirements.txt
├── src/
│   ├── app/                 # код утилиты
│   │   ├── config.py
│   │   ├── loader.py
│   │   ├── parser.py
│   │   ├── comparator.py
│   │   ├── integrator.py
│   │   └── main.py
│   └── data/                # Google API ключи/токены
│       ├── credentials.json
│       └── token.json
└── var/                     # артефакты выполнения
├── tmp/
│   └── raw\.ics
├── state/
│   └── last\_week\_snapshot.json
└── logs/
└── cron.log

````

## Установка
1. Клонировать проект:
   ```bash
   git clone https://github.com/yourname/ics-sync.git
   cd ics-sync
````

2. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Получить `credentials.json` в [Google Cloud Console](https://console.cloud.google.com/)
   (тип приложения — **Desktop App**, включён Calendar API).
   Сохранить в `src/data/credentials.json`.

4. На первом запуске откроется окно браузера для авторизации. После неё создастся `src/data/token.json`.

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

## Примечания

* `credentials.json` не коммитится! Держи его локально.
* Если нужно поменять календарь — укажи `CALENDAR_ID` в `.env` или через переменные окружения.
* В `parser.py` можно указать свой `timeZone` (например, `"Asia/Barnaul"`).

---

✍️ Этот README — базовый каркас. Можешь дописать сюда: скриншоты календаря, нюансы установки в Linux/Windows, или раздел FAQ (например, про ошибки `invalid_grant` и `Missing time zone definition`).

```

---

Хочешь, я добавлю в README ещё раздел “Отладка” с типичными ошибками и их решениями (типа тех, что мы уже прошли: `invalid_grant`, `400 Bad Request` и пр.)?
```
