from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, DeclarativeBase
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    id: Any
    __name__ : str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class VideoFiles(Base):
    __tablename__ = "main"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    file_path: Mapped[str]
    status: Mapped[str]


class Violations(Base):
    __tablename__ = "violations"

    id: Mapped[int] = mapped_column(primary_key=True)
    main_id: Mapped[int] = mapped_column(ForeignKey("main.id"))
    photo: Mapped[str]
    video: Mapped[str]
    category: Mapped[str]
    confidence: Mapped[str]
    datetime: Mapped[datetime]
    camera: Mapped[str]
    field: Mapped[str]
    well_pad: Mapped[str]
    color: Mapped[str]
    sn: Mapped[int]


class CompleteFiles(Base):
    __tablename__ = "complete_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    main_id: Mapped[int] = mapped_column(ForeignKey("main.id"))
    name_complete_file: Mapped[str]
    path_complete_file: Mapped[str]


class CompletePngFiles(Base):
    __tablename__ = "complete_png_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    main_id: Mapped[int] = mapped_column(ForeignKey("main.id"))
    name_complete_png_file: Mapped[str]
    path_complete_png_file: Mapped[str]
