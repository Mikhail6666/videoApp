from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/page", tags=["page"])


@router.get("/", response_class=HTMLResponse)
async def get_general_page():
    with open("templates/index2.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

