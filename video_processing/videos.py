from ultralytics import YOLO

from video_processing.analyze_frames import analyze_frames
from video_processing.extract_video_segments import extract_video_segments

output_folder = '/home/mikhail/PycharmProjects/videoApp/complete_files'

def process_and_stream_video(repo, video_file_id, complete_video_file_repository, complete_png_file_repository):
    model = YOLO("best.pt")
    video_file = repo.get_video_file(video_file_id)
    frame_number = []
    results = model(video_file.file_path, stream=True, conf=0.3, iou=0.2)
    frame_counter = 0
    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])  # Класс предсказания
            if cls == 6:
                frame_number.append(frame_counter)
        frame_counter += 1
    if frame_number:
        frame_result = analyze_frames(frame_number)
        extract_video_segments(video_file.file_path,
                               frame_result,
                               output_folder,
                               video_file_id,
                               complete_video_file_repository,
                               complete_png_file_repository)
    else:
        return {"frame_number": f"None"}
