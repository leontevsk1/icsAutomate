# src/app/comparator.py
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Any
from pprint import pprint

def load_snapshot(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))

def save_snapshot(path: Path, events: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")

def _key(ev: Dict[str, Any]) -> str:
    base = f"{ev.get('summary','')}|{ev.get('start',{}).get('dateTime','')}|{ev.get('location','')}"
    return hashlib.sha1(base.encode()).hexdigest()

def compare(old: List[Dict[str, Any]], new: List[Dict[str, Any]]
           ) -> Tuple[List[Dict], List[Dict], List[Tuple[Dict, Dict]]]:
    old_map = {_key(e): e for e in old}
    new_map = {_key(e): e for e in new}
    to_add = [new_map[k] for k in new_map.keys() - old_map.keys()]
    to_del = [old_map[k] for k in old_map.keys() - new_map.keys()]
    to_upd = []
    for k in new_map.keys() & old_map.keys():
        if json.dumps(new_map[k], sort_keys=True) != json.dumps(old_map[k], sort_keys=True):
            to_upd.append((old_map[k], new_map[k]))
    return to_add, to_del, to_upd

if __name__ == "__main__":
    # Пример: python -m app.comparator old.json new.json
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m app.comparator old.json new.json")
        raise SystemExit(1)
    old = load_snapshot(Path(sys.argv[1]))
    new = load_snapshot(Path(sys.argv[2]))
    a, d, u = compare(old, new)
    print(f"+{len(a)}  -{len(d)}  ~{len(u)}")
    if a or d or u:
        print("Added:"); pprint(a)
        print("Deleted:"); pprint(d)
        print("Updated:"); pprint(u)
