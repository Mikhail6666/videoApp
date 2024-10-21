from handlers.pages import router as pages_router
from handlers.files import router as files_router
from handlers.download import router as download_router
from handlers.api import router as api_router

routers = [api_router, pages_router, files_router, download_router]