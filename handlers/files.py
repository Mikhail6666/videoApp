from typing import Annotated
from fastapi import APIRouter, File, UploadFile, Depends, BackgroundTasks
from video_processing import process_and_stream_video, create_file
from dependency import get_video_files_repository, get_complete_video_files_repository, get_complete_png_files_repository
from repository import VideoFileRepository, CompleteFileRepository, CompletePngFileRepository
from schema.video_file import VideoFileSchema

router = APIRouter(prefix="/file", tags=["file"])

@router.post("/uploadfile/")
async def create_upload_file(background_tasks: BackgroundTasks,
        video_file_repository: Annotated[VideoFileRepository, Depends(get_video_files_repository)],
        complete_video_file_repository: Annotated[CompleteFileRepository,Depends(get_complete_video_files_repository)],
        complete_png_file_repository: Annotated[CompletePngFileRepository,Depends(get_complete_png_files_repository)],
        file: UploadFile = File(...)):
    # Сохранения файла на диск
    path_file = create_file(file)

    video_file = VideoFileSchema(
        name=file.filename,
        file_path=path_file,
        status="Download"
    )
    video_file_id = video_file_repository.create_video_file(video_file)

    background_tasks.add_task(process_and_stream_video,video_file_repository,video_file_id,complete_video_file_repository,complete_png_file_repository)


    return {"message": f"Successfully uploaded {file.filename}"}


@router.get(
    "/all",
    response_model=list[VideoFileSchema]
)
async def get_video_files(video_file_repository: Annotated[VideoFileRepository, Depends(get_video_files_repository)]):
    video_files = video_file_repository.get_video_files()
    return video_files


@router.get(
    "/get_video_file/{video_file_id}",
    response_model=VideoFileSchema
)
async def get_video_file(video_file_id: int, video_file_repository: Annotated[VideoFileRepository, Depends(get_video_files_repository)]):
    video_file = video_file_repository.get_video_file(video_file_id)
    return video_file


@router.post(
    '/video_file',
    response_model=VideoFileSchema
)
async def create_video_file(
    video_file: VideoFileSchema,
    video_file_repository: Annotated[VideoFileRepository, Depends(get_video_files_repository)]
):
    video_file_id = video_file_repository.create_video_file(video_file)
    video_file.id = video_file_id
    return video_file_repository.get_video_file(video_file.id)


@router.patch(
    '/{video_file_id}',
    response_model=VideoFileSchema
)
async def path_video_file(
    video_file_id: int,
    video_file: VideoFileSchema,
    video_file_repository: Annotated[VideoFileRepository, Depends(get_video_files_repository)]
):
    return video_file_repository.update_video_file(video_file_id, video_file)
