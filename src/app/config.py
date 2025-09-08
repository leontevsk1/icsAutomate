# src/app/config.py
from dataclasses import dataclass
from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[2]  # корень проекта
SRC_DIR  = ROOT_DIR / "src"
APP_DIR  = SRC_DIR / "app"
DATA_DIR = SRC_DIR / "data"                     # credentials.json, token.json
VAR_DIR  = ROOT_DIR / "var"                     # артефакты запуска
STATE_DIR= VAR_DIR / "state"
TMP_DIR  = VAR_DIR / "tmp"

STATE_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR.mkdir(parents=True, exist_ok=True)

@dataclass(frozen=True)
class Config:
    # базовые параметры
    ICS_URL: str = os.getenv("ICS_URL", "https://www.asu.ru/timetable/students/14/2129441347/?file=2129441347.ics")
    CALENDAR_ID: str = os.getenv("CALENDAR_ID", "primary")
    WINDOW_DAYS: int = int(os.getenv("WINDOW_DAYS", "7"))

    # пути к файлам
    RAW_ICS_PATH: Path = TMP_DIR / "raw.ics"
    SNAPSHOT_PATH: Path = STATE_DIR / "last_week_snapshot.json"

    # gcal креды/токен
    CREDENTIALS_PATH: Path = DATA_DIR / "credentials.json"
    TOKEN_PATH: Path = DATA_DIR / "token.json"

CFG = Config()

if __name__ == "__main__":
    print("Config:")
    print("  ICS_URL        =", CFG.ICS_URL)
    print("  CALENDAR_ID    =", CFG.CALENDAR_ID)
    print("  WINDOW_DAYS    =", CFG.WINDOW_DAYS)
    print("  RAW_ICS_PATH   =", CFG.RAW_ICS_PATH)
    print("  SNAPSHOT_PATH  =", CFG.SNAPSHOT_PATH)
    print("  CREDENTIALS    =", CFG.CREDENTIALS_PATH)
    print("  TOKEN          =", CFG.TOKEN_PATH)
