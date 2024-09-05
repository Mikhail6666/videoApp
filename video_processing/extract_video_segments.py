import ffmpeg
import os

from schema.complete_video_file import CompleteVideoFileSchema
from schema.complete_png_file import CompletePngFileSchema


def extract_video_segments(
        video_path,
        frame_ranges,
        output_folder,
        video_file_id,
        complete_video_file_repository,
        complete_png_file_repository
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем имя исходного файла без расширения
    file_name = os.path.splitext(os.path.basename(video_path))[0]

    for i, (start_frame, end_frame) in enumerate(frame_ranges):
        frame_number = start_frame + (end_frame - start_frame)//2
        output_path = os.path.join(output_folder, f'{file_name}_{i}.mp4')
        complete_video_file = CompleteVideoFileSchema(
            main_id=video_file_id,
            name_complete_file=f'{file_name}_{i}.mp4',
            path_complete_file=output_path
        )

        (
            ffmpeg
            .input(video_path)
            .trim(start_frame=start_frame, end_frame=end_frame)
            .setpts('PTS-STARTPTS')
            .output(output_path)
            .run(cmd='ffmpeg', overwrite_output=True)  # Указываем явно команду ffmpeg
        )
        complete_video_file_repository.create_complete_video_file(complete_video_file)

        output_path = os.path.join(output_folder, f'{file_name}_{i}.png')
        complete_png_file = CompletePngFileSchema(
            main_id=video_file_id,
            name_complete_png_file=f'{file_name}_{i}.png',
            path_complete_png_file=output_path
        )

        (
            ffmpeg
            .input(video_path)
            .filter('select', f'eq(n,{frame_number})')
            .output(output_path, vframes=1)
            .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
        )
        complete_png_file_repository.create_complete_png_file(complete_png_file)

if __name__ == "__main__":
    # Пример использования
    video_path = '/home/mikhail/PycharmProjects/videoApp/upload_files/krs.mp4'
    frame_ranges = [[277, 437]]
    output_folder = '/home/mikhail/PycharmProjects/videoApp/complete_files'

    extract_video_segments(video_path, frame_ranges, output_folder)
