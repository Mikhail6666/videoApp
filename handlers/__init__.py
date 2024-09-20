from handlers.pages import router as pages_router
from handlers.files import router as files_router
from handlers.download import router as download_router

routers = [pages_router, files_router, download_router]