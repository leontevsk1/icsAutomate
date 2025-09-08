# src/app/main.py
import sys, json
from pathlib import Path

from src.app.config import CFG
from src.app.loader import download_ics
from src.app.parser import parse_ics
from src.app.comparator import load_snapshot, save_snapshot, compare
from src.app.integrator import (
    get_authenticated_service, rfc3339_now_end,
    list_events_in_window, delete_events_by_ids, insert_events
)

def run_full() -> int:
    print("=== FULL ===")
    ok = download_ics(CFG.ICS_URL, CFG.RAW_ICS_PATH)
    if not ok and not CFG.RAW_ICS_PATH.exists():
        print("[full] no ICS available")
        return 2

    events = parse_ics(str(CFG.RAW_ICS_PATH), window_days=CFG.WINDOW_DAYS)
    print(f"[full] parsed events: {len(events)}")

    svc = get_authenticated_service()
    tmin, tmax = rfc3339_now_end(CFG.WINDOW_DAYS)
    existing = list_events_in_window(svc, CFG.CALENDAR_ID, tmin, tmax)
    print(f"[full] calendar has {len(existing)} events in window → replace")

    delete_events_by_ids(svc, CFG.CALENDAR_ID, [e["id"] for e in existing])
    insert_events(svc, CFG.CALENDAR_ID, events)

    save_snapshot(CFG.SNAPSHOT_PATH, events)
    print(f"[full] snapshot saved to {CFG.SNAPSHOT_PATH}")
    return 0

def run_diff() -> int:
    print("=== DIFF ===")
    prev = load_snapshot(CFG.SNAPSHOT_PATH)

    ok = download_ics(CFG.ICS_URL, CFG.RAW_ICS_PATH)
    if not ok and not CFG.RAW_ICS_PATH.exists():
        print("[diff] no ICS available")
        return 2

    current = parse_ics(str(CFG.RAW_ICS_PATH), window_days=CFG.WINDOW_DAYS)
    print(f"[diff] parsed events: {len(current)}")

    add, delete, update = compare(prev, current)
    changed = len(add) + len(delete) + len(update)
    print(f"[diff] changes: +{len(add)} -{len(delete)} ~{len(update)}")

    if changed == 0:
        print("[diff] nothing to do")
        return 0

    svc = get_authenticated_service()
    tmin, tmax = rfc3339_now_end(CFG.WINDOW_DAYS)
    existing = list_events_in_window(svc, CFG.CALENDAR_ID, tmin, tmax)
    print(f"[diff] calendar has {len(existing)} events in window → replace")

    delete_events_by_ids(svc, CFG.CALENDAR_ID, [e["id"] for e in existing])
    insert_events(svc, CFG.CALENDAR_ID, current)

    save_snapshot(CFG.SNAPSHOT_PATH, current)
    print(f"[diff] snapshot updated")
    return 0

def main(argv):
    mode = argv[1] if len(argv) > 1 else "full"
    if mode == "full":
        return run_full()
    elif mode == "diff":
        return run_diff()
    else:
        print("Usage: python -m src.app.main [full|diff]")
        return 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
