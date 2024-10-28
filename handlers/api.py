import os
from datetime import datetime

import fastapi
from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated
from fastapi.responses import StreamingResponse
from dependency import get_violation_repository
from repository import ViolationRepository
from schema import ViolationsSchema, GetPhotoFile, GetVideoFile

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/get_list_of_events",
            response_model=list[ViolationsSchema],
            summary="Список нарушений",
            description="Получение полного списка нарушений")
async def get_list_of_events(start_date: datetime,
                    end_date: datetime,sn: int,
                    violations_repository: Annotated[ViolationRepository, Depends(get_violation_repository)]):
    violations = violations_repository.get_violations_from_time(start_date, end_date, sn)
    # if not violations:
    #     raise HTTPException(status_code=404, detail="Violation not found")

    return violations


@router.get("/get_count_of_events",
            summary="Кол-во нарушений",
            description="Получение кол-во нарушений")
async def get_count_of_events(start_date: datetime,
                    end_date: datetime,
                    violations_repository: Annotated[ViolationRepository, Depends(get_violation_repository)]):
    violations = violations_repository.get_amount_violations_from_time(start_date, end_date)
    if not violations:
        raise HTTPException(status_code=404, detail="Violation not found")

    return violations


@router.post("/photo",
             summary="Фото",
             description="Получение фотографии нарушения")
async def get_photo(photo: GetPhotoFile = fastapi.Body(description="Path to the image file")):
    if not os.path.exists(photo.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(photo.file_path, "rb") as file:
        return Response(file.read(), media_type="image/jpeg")


@router.post("/video",
             summary="Видео",
             description="Получение видео нарушения")
async def get_video(video: GetVideoFile = fastapi.Body(description="Path to the video file")):
    if not os.path.exists(video.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    def stream_video():
        with open(video.file_path, "rb") as file:
            while chunk := file.read(1024 * 1024):  # Читаем по 1 МБ
                yield chunk

    return StreamingResponse(stream_video(), media_type="video/mp4")
