from typing import Union
from fastapi.responses import HTMLResponse, JSONResponse
import json

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/analyze")
def analyze(task):
    
    return {"title": "essay", "estimated_time": "7 hours", "risk": "high effort task"}