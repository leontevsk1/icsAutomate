# src/app/integrator.py
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from src.app.config import CFG

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_authenticated_service():
    creds = None
    token_path = CFG.TOKEN_PATH
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[gcal] refreshing token")
            creds.refresh(Request())
        else:
            print("[gcal] first auth — opening browser")
            flow = InstalledAppFlow.from_client_secrets_file(str(CFG.CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding="utf-8")
        print(f"[gcal] token saved to {token_path}")

    return build("calendar", "v3", credentials=creds, cache_discovery=False)

def rfc3339_now_end(days: int):
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)
    # RFC3339: UTC → суффикс Z
    return now.isoformat(timespec="seconds").replace("+00:00", "Z"), \
           end.isoformat(timespec="seconds").replace("+00:00", "Z")

def list_events_in_window(service, calendar_id: str, time_min: str, time_max: str) -> List[Dict[str, Any]]:
    items, page_token = [], None
    while True:
        resp = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
            pageToken=page_token,
            maxResults=2500,
        ).execute()
        items.extend(resp.get("items", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return items

def delete_events_by_ids(service, calendar_id: str, ids: List[str]) -> None:
    for eid in ids:
        try:
            service.events().delete(calendarId=calendar_id, eventId=eid).execute()
            print(f"[gcal] deleted: {eid}")
        except Exception as e:
            print(f"[gcal] delete failed for {eid}: {e}")

def insert_events(service, calendar_id: str, events: List[Dict[str, Any]]) -> None:
    for ev in events:
        try:
            service.events().insert(calendarId=calendar_id, body=ev).execute()
            print(f"[gcal] inserted: {ev.get('summary')} @ {ev.get('start',{}).get('dateTime')}")
        except Exception as e:
            print(f"[gcal] insert failed: {e}")

if __name__ == "__main__":
    svc = get_authenticated_service()
    tmin, tmax = rfc3339_now_end(7)
    exist = list_events_in_window(svc, CFG.CALENDAR_ID, tmin, tmax)
    print(f"[gcal] events in window: {len(exist)}")
