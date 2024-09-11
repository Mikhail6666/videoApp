import asyncio
from database_videos.process_videos import process_videos
from database_videos.scan_directory import scan_directory


async def main_loop(folder_path, interval=10):
    while True:
        # Сканируем директорию на наличие новых файлов
        scan_directory(folder_path)
        # Обрабатываем файлы
        process_videos()
        # Ждем интервал времени перед следующим сканированием
        # print(f"Waiting for {interval} seconds before next scan...")
        await asyncio.sleep(interval)
