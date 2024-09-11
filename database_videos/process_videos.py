import sqlite3


def process_videos():
    conn = sqlite3.connect('video_archive.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM videos WHERE processed = 0')
    videos = cursor.fetchall()
    for video in videos:
        file_path = video[1]
        print(f"Processing video: {file_path}")
        # Здесь можно добавить логику обработки видео
        # Например, вызов внешнего сервиса или библиотеки для обработки видео

        # После обработки обновляем статус
        cursor.execute('UPDATE videos SET processed = 1 WHERE file_path = ?', (file_path,))
        print(f"Processed video: {file_path}")

    conn.commit()
    conn.close()
