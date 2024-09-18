import cv2
import ffmpeg
import os
import re
from schema import ViolationsSchema


def get_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видеофайл.")
        return {"frame_number": "None"}
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    return frame_rate


def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split('-'))
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}-{minutes:02}-{seconds:02}"


def calculate_frame_time(start_time_str, fps_str, frame_number):
    start_time_seconds = time_to_seconds(start_time_str)
    # frame_number = int(frame_number_str)
    frame_time_seconds = start_time_seconds + (frame_number / fps_str)
    frame_time_str = seconds_to_time(frame_time_seconds)
    return frame_time_str


def get_date_and_time(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', filename)
    print(filename)
    if match:
        datetime_str = match.group(1)
        date_str, time_str = datetime_str.split('_')
        return date_str, time_str

def extract_video_segments(
        video_path,
        frame_result,
        output_folder,
        video_file_id,
        violations_repository
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем имя исходного файла без расширения
    file_name = os.path.splitext(os.path.basename(video_path))[0]
    fps = get_fps(video_path)
    date_str, time_str = get_date_and_time(file_name)

    for i in range(0, len(frame_result)):
        frame_number = frame_result[i][2][0]
        video_output_path = os.path.join(output_folder, f'{file_name}_{i}.mp4')
        time_str_result = calculate_frame_time(time_str, fps, frame_number)
        violation = ViolationsSchema(
            main_id=video_file_id,
            video=video_output_path,
            category='head',
            confidence=str(frame_result[i][2][1]),
            camera="1",
            date=date_str,
            time=time_str_result
        )

        (
            ffmpeg
            .input(video_path)
            .trim(start_frame=frame_result[i][0], end_frame=frame_result[i][1])
            .setpts('PTS-STARTPTS')
            .output(video_output_path)
            .run(cmd='ffmpeg', overwrite_output=True)  # Указываем явно команду ffmpeg
        )

        png_output_path = os.path.join(output_folder, f'{file_name}_{i}.png')
        violation.photo = png_output_path

        (
            ffmpeg
            .input(video_path)
            .filter('select', f'eq(n,{frame_number})')
            .output(png_output_path, vframes=1)
            .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
        )
        violations_repository.create_violation(violation)

if __name__ == "__main__":
    # Пример использования
    video_path = '/home/mikhail/PycharmProjects/videoApp/upload_files/krs.mp4'
    frame_result = [[277, 437]]
    output_folder = '/home/mikhail/PycharmProjects/videoApp/complete_files'

    extract_video_segments(video_path, frame_result, output_folder)
