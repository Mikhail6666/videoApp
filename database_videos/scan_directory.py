from datetime import datetime
import sqlite3
import os
video_archive_db = os.getenv("VIDEO_ARCHIVE_DB")


def scan_directory(folder_path):
    conn = sqlite3.connect(video_archive_db)
    cursor = conn.cursor()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Проверяем, что файл имеет расширение .mp4
            if not file.lower().endswith('.mp4'):
                continue

            # Проверяем размер файла
            file_size = os.path.getsize(file_path)
            if file_size <= 1024 * 1024:  # 1 мегабайт = 1024 * 1024 байт
                continue

            cursor.execute('SELECT * FROM videos WHERE file_path = ?', (file_path,))
            if cursor.fetchone() is None:
                added_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('INSERT INTO videos (file_path, added_date) VALUES (?, ?)', (file_path, added_date))

    conn.commit()
    conn.close()

# scan_directory('/mnt/network_share/ТКРС_2_кам2/2024/09/12')