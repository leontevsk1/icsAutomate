from pathlib import Path
import requests
from src.app.config import CFG

def download_ics(url: str, dest: Path, timeout: int = 20) -> bool:
    print(f"[loader] GET {url}")
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "ScheduleSync/1.0"})
    if r.status_code != 200:
        print(f"[loader] HTTP {r.status_code}")
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)
    print(f"[loader] saved to {dest} ({len(r.content)} bytes)")
    return True

if __name__ == "__main__":
    ok = download_ics(CFG.ICS_URL, CFG.RAW_ICS_PATH)
    print("OK" if ok else "FAIL")
