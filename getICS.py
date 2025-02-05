import wget
import asyncio
async def download():
    loop = asyncio.get_running_loop()
    # Используем run_in_executor для выполнения синхронного wget.download асинхронно
    await loop.run_in_executor(None, wget.download, 'https://www.asu.ru/timetable/students/14/2129441347/?file=2129441347.ics', "C:/Users/artem/Документы/MyPy/2129441347.ics")
