from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database import CompleteFiles
from schema.complete_video_file import CompleteVideoFileSchema


class CompleteFileRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_complete_video_files(self) -> list[CompleteVideoFileSchema]:
        with self.db_session as session:
            video_files: list[CompleteVideoFileSchema] = session.execute(select(CompleteFiles)).scalars().all()
            return video_files

    def get_complete_video_file(self, video_file_id: int) -> CompleteVideoFileSchema | None:
        with self.db_session as session:
            video_file: CompleteVideoFileSchema = session.execute(select(CompleteFiles).where(CompleteFiles.id == video_file_id)
                                                     ).scalar_one_or_none()
            return video_file

    def create_complete_video_file(self, video_file: CompleteVideoFileSchema) -> int:
        video_file_model = CompleteFiles(
            main_id=video_file.main_id,
            name_complete_file=video_file.name_complete_file,
            path_complete_file=video_file.path_complete_file)
        with self.db_session as session:
            session.add(video_file_model)
            session.commit()
            return video_file_model.id


    def update_complete_video_file(self, video_file_id: int, video_file: CompleteVideoFileSchema) -> CompleteVideoFileSchema | None:
        query = (update(CompleteFiles).where(CompleteFiles.id == video_file_id)
                 .values(main_id=video_file.main_id,
                         name_complete_file=video_file.name_complete_file,
                         path_complete_file=video_file.path_complete_file
                ).returning(CompleteFiles.id))
        with self.db_session as session:
            video_file_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_complete_video_file(video_file_id)


    def delete_complete_video_file(self, video_file_id: int) -> None:
        query = delete(CompleteFiles).where(CompleteFiles.id == video_file_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()
