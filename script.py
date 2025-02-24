from icalendar import Calendar
import os
import datetime
import wget
import asyncio
import pg
from user_secr import secrets as s
import calendarService

async def download():
    loop = asyncio.get_running_loop()
    # Используем run_in_executor для выполнения синхронного wget.download асинхронно
    if await loop.run_in_executor(None, wget.download, 'https://www.asu.ru/timetable/students/14/2129441347/?file=2129441347.ics'):
        print(' Succesfully downloaded')
    else:
        print('Error')

def get_last_date():
    secrets = s()
    conn = pg.create_connection(secrets)
    query = 'SELECT * FROM date'
    last_date = pg.execute_query(conn, query)
    if not last_date:
        print('Empty Data')
        last_date = [datetime.datetime.now()]
        print(last_date)
        query = f"INSERT INTO date(date) VALUES ('{last_date[0]}')"
        pg.insert_query(conn, query)
    
    pg.close_connection(conn)
    
    datetime_ics = datetime.datetime.combine(last_date[0], datetime.time(0,0,0), tzinfo=datetime.timezone.utc)
    #ics_format_date = datetime_with_time.strftime('%Y-%m-%dT%H:%M:%S%z')
    # Добавляем временную зону (UTC)
    #ics_format_date += '+07:00'
    return datetime_ics


def parse_ics(file_path):
    date = get_last_date()
    with open(file_path, 'rb') as f:
        cal = Calendar.from_ical(f.read())
    events = []
    for component in cal.walk():
        if component.name == 'VEVENT' and component.get('dtstart').dt>date:
            events.append({
                'summary': component.get('summary'),
                'start': {'dateTime': component.get('dtstart').dt.isoformat()},
                'end': {'dateTime': component.get('dtend').dt.isoformat()},
                'description': component.get('description'),
                'location': component.get('location')
            })
    os.remove(file_path)
    return events

def main(path):
    events = parse_ics(path)
    new_date = events[-1]['start']['dateTime']
    dt = datetime.datetime.fromisoformat(new_date)
    date = dt.strftime('%Y-%m-%d')
    secrets = s()
    conn = pg.create_connection(secrets)
    query = f"UPDATE date SET date = '{date}'"
    pg.insert_query(conn,query)
    pg.close_connection(conn)
    print(date)
    service = calendarService.get_authenticated_service()
    id = 'primary'
    calendarService.upload_to_gcal(service, id, events)
    

if __name__ == '__main__':
    asyncio.run(download())
    print(main('/home/artem/pyenvs/IcsScriptPG/2129441347.ics'))
    