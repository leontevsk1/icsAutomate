import re
from tkinter import filedialog
from pathlib import Path
from datetime import datetime
import os
import setDB
from setDB import last_date
from getICS import download
import asyncio
import webbrowser
import uploadInCalendar
import KMP

if last_date:
    current_datetime = last_date[0][0]
else:
    print("Нет данных в результате запроса.")
    current_datetime = datetime.now()
    conn = setDB.create_connection(setDB.host, setDB.user,setDB.pword,setDB.db_name)
    query = f"INSERT INTO date(date) VALUES ('{current_datetime}')"
    setDB.execute_query(conn,query)
    conn.close()
   
current_dtstart_format = current_datetime.strftime("%Y-%m-%d")

# Функция записи в ics файл
def ICSCreator(arr):
    path = filedialog.askdirectory()  # Получаем путь, куда сохранять файлы
    if path != "":
        # Создание файла для основного текста
        file_path = os.path.join(path, f"{current_dtstart_format}.ics")
        with open(file_path, "w+", encoding='utf-8') as my_file:
            for c in arr:
                my_file.write(c)  # Записываем все символы (переносы строк, пробелы и слова)
    
    print(f"Файлы сохранены в: {path}")
    return path
    

asyncio.run(download())

while True:
    filePath = Path("C:/Users/artem/Документы/MyPy/2129441347.ics")
    if filePath.suffix == ".ics" and filePath.exists():
        with open(filePath, 'r', encoding='utf-8') as file:
            data = file.read()
            break
    elif filePath != "" or filePath != " ":
        break
    else:
        print("Выберите корректный файл в формате .ics")



# Регулярное выражение для поиска блока от "BEGIN:VCALENDAR" до первого "BEGIN:VEVENT"
pattern = re.compile(r'(BEGIN:VCALENDAR.*?)(?=BEGIN:VEVENT)', re.DOTALL)
match = pattern.search(data)

# Найти и сохранить фрагмент
if match:
    calendar_fragment = match.group(0)  # Сохраняем фрагмент

    # Удаляем фрагмент из исходной строки
    data = data.replace(calendar_fragment, '', 1)  # Удаляем только первое вхождение

# Компилируем регулярное выражение для поиска последнего DTSTART
# Регулярное выражение для захвата только даты и времени
pattern = re.compile(r'DTSTART(?:;TZID=[^:]+)?:([\dT]+)')
match = pattern.findall(data)

# Получаем последнее совпадение, если оно существует
if match:
    last_dtstart = match[-1]  # Получаем только дату и время
    # Определяем формат даты и времени в зависимости от длины строки
    dt_format = '%Y%m%dT%H%M%S' if len(last_dtstart) == 15 else '%Y%m%dT%H%M'
    dt = datetime.strptime(last_dtstart, dt_format)
    
    # Форматируем в строку для базы данных
    formatted_date = dt.strftime('%Y-%m-%d')
    print(f'Отформатированная дата для БД: {formatted_date}')
else:
    print('Записи DTSTART не найдены.')
# Регулярное выражение для поиска блоков VEVENT
event_pattern = re.compile(r'BEGIN:VEVENT(.*?)END:VEVENT', re.DOTALL)

# Список для хранения событий в формате [[BEGIN:VEVENT, ..., END:VEVENT], ...]
events_list = []

# Поиск всех блоков событий VEVENT
for match in event_pattern.finditer(data):
    event_block = match.group(0)  # Полный текст блока "BEGIN:VEVENT ... END:VEVENT"
    
    # Разделяем блок на строки и фильтруем пустые строки
    event_lines = [line.strip() for line in event_block.splitlines() if line.strip()]
    
    # Добавляем блок в список событий
    events_list.append(event_lines)
final_list = []
found = False

for index, block in enumerate(events_list):
    for line in block:
        # Проверяем, начинается ли строка с "DTSTART;" и содержит ли текущую дату
        if line.startswith("DTSTART;") and KMP.kmp(current_dtstart_format, line):
            # Как только находим первый блок, соответствующий дате, фиксируем его индекс
            final_list = events_list[index:]
            found = True
            break
    if found:
        break  # Выходим из внешнего цикла, если нужное событие найдено


conn = setDB.create_connection(setDB.host, setDB.user,setDB.pword,setDB.db_name)
query = f"UPDATE date SET date = '{formatted_date}'"
setDB.execute_query(conn,query)
conn.close()
   
res = "\n".join("\n".join(event) for event in final_list)
res = f"{calendar_fragment}\n"+f"{res}\n"+"END:VCALENDAR"
path = ICSCreator(res)
service = uploadInCalendar.get_calendar_service()
events = uploadInCalendar.parse_ics(f'{path}/{current_dtstart_format}.ics')
#print(f'{path}/{current_dtstart_format}')
try:
    uploadInCalendar.upload_to_gcal(service, 'primary', events)
except ValueError as e:
    print(f'Возникла ошибка: {e}')
os.remove('C:/Users/artem/Документы/MyPy/2129441347.ics')
#webbrowser.open('https://calendar.google.com/calendar/u/0/r/settings/export')