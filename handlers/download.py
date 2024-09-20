import os
from fastapi import APIRouter, Response, Depends, HTTPException
from typing import Annotated
from fastapi.responses import StreamingResponse
from dependency import get_violation_repository
from repository import ViolationRepository


router = APIRouter(prefix="/download", tags=["download"])


@router.get("/photo/{file_id}")
async def get_photo(file_id: int,
                    violations_repository: Annotated[ViolationRepository, Depends(get_violation_repository)]):
    violation = violations_repository.get_violation(file_id)
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    file_path = violation.photo

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "rb") as file:
        return Response(file.read(), media_type="image/jpeg")


@router.get("/video/{file_id}")
async def get_video(file_id: int,
                    violations_repository: Annotated[ViolationRepository, Depends(get_violation_repository)]):
    violation = violations_repository.get_violation(file_id)
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    file_path = violation.video

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

        # Открываем файл в двоичном режиме для потоковой передачи
    def stream_video():
        with open(file_path, "rb") as file:
            while chunk := file.read(1024 * 1024):  # Читаем по 1 МБ
                yield chunk

    return StreamingResponse(stream_video(), media_type="video/mp4")
