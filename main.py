from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from handlers import routers
import asyncio
from database_videos.main_loop import main_loop
import os
folder_videos = os.getenv("FOLDER_VIDEOS")
from fastapi.middleware.cors import CORSMiddleware


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Действия при старте приложения
#     folder_path = folder_videos
#     asyncio.create_task(main_loop(folder_path))
#     print("Приложение запущено")
#     yield
#     print("Приложение завершено")
#
#     # Действия при завершении приложения
#     # Например, остановка задач, закрытие соединений и т.д.

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://videoanalytics.driveintech.ru",
        "https://ns.driveintech.ru/"
    ],  # Разрешить запросы с localhost:8080
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP-методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)
# app = FastAPI(lifespan=lifespan)
for router in routers:
    app.include_router(router)

@app.get("/")
async def redirect_from():
    return RedirectResponse(url="/page/")
