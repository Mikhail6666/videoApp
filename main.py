from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from handlers import routers
import asyncio
from database_videos.main_loop import main_loop
from settings import FOLDER_VIDEOS

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте приложения
    folder_path = FOLDER_VIDEOS
    asyncio.create_task(main_loop(folder_path))
    print("Приложение запущено")
    yield
    print("Приложение завершено")

    # Действия при завершении приложения
    # Например, остановка задач, закрытие соединений и т.д.


app = FastAPI(lifespan=lifespan)
for router in routers:
    app.include_router(router)

@app.get("/")
async def redirect_from():
    return RedirectResponse(url="/page/")
