import os
from datetime import datetime
import sqlite3


def scan_directory(folder_path):
    conn = sqlite3.connect('video_archive.db')
    cursor = conn.cursor()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            cursor.execute('SELECT * FROM videos WHERE file_path = ?', (file_path,))
            if cursor.fetchone() is None:
                added_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('INSERT INTO videos (file_path, added_date) VALUES (?, ?)', (file_path, added_date))

    conn.commit()
    conn.close()
