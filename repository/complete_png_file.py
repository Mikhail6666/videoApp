from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database import CompletePngFiles
from schema.complete_png_file import CompletePngFileSchema


class CompletePngFileRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_complete_png_files(self) -> list[CompletePngFileSchema]:
        with self.db_session as session:
            png_files: list[CompletePngFileSchema] = session.execute(select(CompletePngFiles)).scalars().all()
            return png_files

    def get_complete_png_file(self, png_file_id: int) -> CompletePngFileSchema | None:
        with self.db_session as session:
            png_file: CompletePngFileSchema = session.execute(select(CompletePngFiles).where(CompletePngFiles.id == png_file_id)
                                                     ).scalar_one_or_none()
            return png_file

    def create_complete_png_file(self, png_file: CompletePngFileSchema) -> int:
        png_file_model = CompletePngFiles(
            main_id=png_file.main_id,
            name_complete_png_file=png_file.name_complete_png_file,
            path_complete_png_file=png_file.path_complete_png_file)
        with self.db_session as session:
            session.add(png_file_model)
            session.commit()
            return png_file_model.id


    def update_complete_png_file(self, png_file_id: int, png_file: CompletePngFileSchema) -> CompletePngFileSchema | None:
        query = (update(CompletePngFiles).where(CompletePngFiles.id == png_file_id)
                 .values(main_id=png_file.main_id,
                         name_complete_png_file=png_file.name_complete_png_file,
                         path_complete_png_file=png_file.path_complete_png_file
                ).returning(CompletePngFiles.id))
        with self.db_session as session:
            png_file_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_complete_png_file(png_file_id)


    def delete_complete_png_file(self, png_file_id: int) -> None:
        query = delete(CompletePngFiles).where(CompletePngFiles.id == png_file_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()
