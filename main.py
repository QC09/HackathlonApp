from typing import Union
from fastapi.responses import HTMLResponse, JSONResponse
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from service import googleAIClient

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/task")
def read_task_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="today.html",
    )

# @app.get('/')
# def read_root(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html",
#         context={"content": "Your content here", "text": "OK"}
#     )

@app.get("/analyze")
def analyze_task(q: str):
    response = googleAIClient.generate_response(q)

    return response
