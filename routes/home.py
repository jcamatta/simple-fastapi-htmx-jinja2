from typing import Annotated
import time

from fastapi import Request, UploadFile, File
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse

from core.config import templates

predictions = {}

model = "vision:1.0.0"

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(name="/pages/home.html", request=request, context={})


@router.get("/models/vision", response_class=HTMLResponse)
async def all_prediction(request: Request):
    context = {
        "predictions": predictions,
        "model": model
    }
    return templates.TemplateResponse(name="/partials/predictions.html", 
                                      request=request, 
                                      context=context)

@router.post("/models/vision")
async def vision_predict(image: UploadFile):

    if image.filename in predictions:
        return predictions[image.filename]["prediction"]
    
    predictions[image.filename] = {
        "image": image.filename,
        "prediction": image.filename.split(".")[0],
        "datetime": time.asctime(),
        "model": model,
    }

    time.sleep(3)
    return predictions[image.filename]["prediction"]