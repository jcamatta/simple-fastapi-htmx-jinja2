from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from core.config import settings

from routes.home import router as home_router


app = FastAPI(
    title=settings.app_title,
    root_path=settings.root_path,
)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

# =======> ROUTERS
app.include_router(home_router)


