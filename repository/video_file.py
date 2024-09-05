from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database import VideoFiles
from schema.video_file import VideoFileSchema


class VideoFileRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_video_files(self) -> list[VideoFileSchema]:
        with self.db_session as session:
            video_files: list[VideoFileSchema] = session.execute(select(VideoFiles)).scalars().all()
        return video_files

    def get_video_file(self, video_file_id: int) -> VideoFileSchema | None:
        with self.db_session as session:
            video_file: VideoFileSchema = session.execute(select(VideoFiles).where(VideoFiles.id == video_file_id)
                                                     ).scalar_one_or_none()
        return video_file

    def create_video_file(self, video_file: VideoFileSchema) -> int:
        video_file_model = VideoFiles(
            name=video_file.name,
            file_path=video_file.file_path,
            status=video_file.status)
        with self.db_session as session:
            session.add(video_file_model)
            session.commit()
            return video_file_model.id


    def update_video_file(self, video_file_id: int, video_file: VideoFileSchema) -> VideoFileSchema | None:
        query = (update(VideoFiles).where(VideoFiles.id == video_file_id)
                 .values(name=video_file.name,
                         file_path=video_file.file_path,
                         status=video_file.status
                ).returning(VideoFiles.id))
        with self.db_session as session:
            video_file_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_video_file(video_file_id)


    def delete_video_file(self, video_file_id: int) -> None:
        query = delete(VideoFiles).where(VideoFiles.id == video_file_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()
