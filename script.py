from icalendar import Calendar
import os
from datetime import datetime
import wget
import asyncio
import pg
from user_secr import secrets as s

async def download():
    loop = asyncio.get_running_loop()
    # Используем run_in_executor для выполнения синхронного wget.download асинхронно
    if await loop.run_in_executor(None, wget.download, 'https://www.asu.ru/timetable/students/14/2129441347/?file=2129441347.ics'):
        print(' succesfully downloaded')
    else:
        print('error')

def get_last_date():
    conn = pg.create_connection()
    query = 'SELECT date FROM date'
    last_date = pg.execute_query(conn, query)
    if last_date is None:
        print('Empty Data')
        last_date = datetime.now()
        query = f"INSERT INTO date(date) VALUES ('{last_date}')"
        pg.execute_query(conn, query)
    pg.close_connection(conn)
    return last_date



def parse_ics(file_path):
    date = get_last_date()
    with open(file_path, 'rb') as f:
        cal = Calendar.from_ical(f.read())
    events = []
    for component in cal.walk():
        if component.name == 'VEVENT' and component.get('dtstart') >= date:
            events.append({
                'summary': component.get('summary'),
                'start': {'dateTime': component.get('dtstart').dt.isoformat()},
                'end': {'dateTime': component.get('dtend').dt.isoformat()},
                'description': component.get('description'),
                'location': component.get('location')
            })
    os.remove(file_path)
    return events

if __name__ == '__main__':
    asyncio.run(download())
    print(parse_ics('/home/artem/pyenvs/IcsScriptPG/2129441347.ics'))