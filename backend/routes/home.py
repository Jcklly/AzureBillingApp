from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/")
def home():
    return RedirectResponse(url="/static/index.html")