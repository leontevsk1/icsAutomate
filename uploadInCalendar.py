from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from icalendar import Calendar
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # Файл для сохранения токенов
    token_file = 'token.json'

    # Если токен уже существует, загрузите его
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # Если токен недействителен или отсутствует, запросите новый
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credit.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Сохраните токен для будущих запросов
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def parse_ics(file_path):
    with open(file_path, 'rb') as f:
        cal = Calendar.from_ical(f.read())
    events = []
    for component in cal.walk():
        if component.name == 'VEVENT':
            events.append({
                'summary': component.get('summary'),
                'start': {'dateTime': component.get('dtstart').dt.isoformat()},
                'end': {'dateTime': component.get('dtend').dt.isoformat()},
                'description': component.get('description'),
                'location': component.get('location')
            })
    return events

def upload_to_gcal(service, calendar_id, events):
    for event in events:
        service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()
        print(f"Event '{event['summary']}' added.")
    print('success')
        