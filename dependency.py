from database import get_db_session
from repository import VideoFileRepository, CompletePngFileRepository, CompleteFileRepository, ViolationRepository

def get_video_files_repository() -> VideoFileRepository:
    db_session = get_db_session()
    return VideoFileRepository(db_session)

def get_complete_video_files_repository() -> CompleteFileRepository:
    db_session = get_db_session()
    return CompleteFileRepository(db_session)

def get_complete_png_files_repository() -> CompletePngFileRepository:
    db_session = get_db_session()
    return CompletePngFileRepository(db_session)

def get_violation_repository() -> ViolationRepository:
    db_session = get_db_session()
    return ViolationRepository(db_session)
