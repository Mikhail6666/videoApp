from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from handlers import routers


app = FastAPI()
for router in routers:
    app.include_router(router)

@app.get("/")
async def redirect_from():
    return RedirectResponse(url="/page/")
