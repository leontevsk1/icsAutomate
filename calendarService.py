from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_authenticated_service():
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Сохраните токен для будущих запросов
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def upload_to_gcal(service, calendar_id, events):
    for event in events:
        try:
            service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            print(f"Event '{event['summary']}' added.")
        except HttpError as e:
            print(f"Ошибка при добавлении события: {e}")
    print('Calendar added successfully')

if __name__ == '__main__':
    print(get_authenticated_service())