import sqlite3
from video_processing import process_and_stream_video
from dependency import get_video_files_repository, get_violation_repository
from repository import VideoFileRepository, ViolationRepository
from schema import VideoFileSchema


async def process_videos():
    conn = sqlite3.connect('video_archive.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM videos WHERE processed = 0')
    videos = cursor.fetchall()

    # Получаем необходимые зависимости вручную
    video_file_repository = get_video_files_repository()
    violation_repository = get_violation_repository()


    for video in videos:
        file_path = video[1]
        print(f"Processing video: {file_path}")
        # Вызов асинхронной функции для загрузки файла
        create_upload_file(video_file_repository,
            violation_repository,
            file_path)
        # После обработки обновляем статус
        cursor.execute('UPDATE videos SET processed = 1 WHERE file_path = ?', (file_path,))
        print(f"Processed video: {file_path}")

    conn.commit()
    conn.close()


def create_upload_file(
        video_file_repository: VideoFileRepository,
        violation_repository: ViolationRepository,
        file_path: str):

    file_name = file_path.split('/')[-1]

    video_file = VideoFileSchema(
        name=file_name,
        file_path=file_path,
        status="Download"
    )
    video_file_id = video_file_repository.create_video_file(video_file)

    process_and_stream_video(video_file_repository,video_file_id,violation_repository)


    return {"message": f"Successfully uploaded {file_name}"}
