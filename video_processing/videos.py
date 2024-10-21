from ultralytics import YOLO
from video_processing.analyze_frames import analyze_frames
from video_processing.extract_video_segments import extract_video_segments
import os
complete_files = os.getenv("COMPLETE_FILES")


def process_and_stream_video(repo, video_file_id, violations_repository):
    model = YOLO("best.pt")
    video_file = repo.get_video_file(video_file_id)
    frame_info = []
    results = model(video_file.file_path, stream=True, conf=0.3, iou=0.2, classes=[6])
    frame_counter = 0
    for result in results:
        for box in result.boxes:
            conf = float(box.conf[0])
            frame_info.append({"frame_number": frame_counter, "confidence": conf})
        frame_counter += 1
    if frame_info:
        frame_result = analyze_frames(frame_info)
        extract_video_segments(video_file.file_path,
                               frame_result,
                               complete_files,
                               video_file_id,
                               violations_repository)
    else:
        return {"frame_number": f"None"}

if __name__ == "__main__":
    pass
