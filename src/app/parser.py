from icalendar import Calendar
from datetime import datetime, timedelta
from pprint import pprint

def parse_ics(file_path: str, window_days: int = 7):
    """
    Возвращает события из ICS на текущую неделю (сейчас + window_days).
    Все datetime приводим к naive (без tzinfo).
    """
    now = datetime.now()
    window_end = now + timedelta(days=window_days)

    with open(file_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

    events = []
    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        dtstart = component.get("dtstart").dt
        dtend = component.get("dtend").dt

        # Приводим всё к datetime без tzinfo
        if not isinstance(dtstart, datetime):
            dtstart = datetime.combine(dtstart, datetime.min.time())
        if not isinstance(dtend, datetime):
            dtend = datetime.combine(dtend, datetime.min.time())
        if dtstart.tzinfo:
            dtstart = dtstart.replace(tzinfo=None)
        if dtend.tzinfo:
            dtend = dtend.replace(tzinfo=None)

        if now <= dtstart < window_end:
            events.append({
                "summary": str(component.get("summary", "")),
                "start": {
                    "dateTime": dtstart.isoformat(),
                    "timeZone": "Asia/Barnaul"},
                "end": {
                    "dateTime": dtend.isoformat(),
                    "timeZone": "Asia/Barnaul"},
                "description": str(component.get("description", "")),
                "location": str(component.get("location", "")),
            })

    events.sort(key=lambda e: e["start"]["dateTime"])
    return events

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "example.ics"
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    pprint(parse_ics(path, days))
