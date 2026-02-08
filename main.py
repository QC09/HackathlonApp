from typing import Union
from fastapi.responses import HTMLResponse, JSONResponse
import json
import os
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from pydantic import BaseModel
from service import googleAIClient

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class AssignmentRequest(BaseModel):
    description: str


def read_data_from_file():
    """Read assignments data from data/data.json file"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    data_file = data_dir / "data.json"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
                return data
            except json.JSONDecodeError:
                return []
    else:
        return []


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.get("/today")
def read_task_page(request: Request):
    data = read_data_from_file()
    return templates.TemplateResponse(
        request=request,
        name="today.html",
        context={"assignments": data}
    )

@app.get("/plan")
def read_plan_page(request: Request):


    data = read_data_from_file()

    return templates.TemplateResponse(
        request=request,
        name="main.html",
        context= {
            "numberOfDeadlines": len(data),
            # "task_1": data[0],
            "assignments": data,
            # "tasks_1": data[0]["tasks"],
        }
    )

# TODO: Create /quiz and /insight to render html file

@app.get("/insights")
def read_insights_page(request:Request):
    return templates.TemplateResponse(
        request = request,
        name = "insights.html",
    )

@app.get("/profile")
def read_profile_page(request:Request):
    return templates.TemplateResponse(
        request=request, 
        name = "profile.html"
    )

@app.get("quiz")
def read_quiz_page(request: Request):
    return templates.TemplatesResponse(
        request = request,
        name = ""
    )

@app.get("/main")
def read_main_page(request: Request):
    data = read_data_from_file()
    print(data)

    return templates.TemplateResponse(
        request=request,
        name="main.html",
        context={"assignments": data}
    )

@app.get("/generate-strategy")
async def generate_strategy():
    data = read_data_from_file()
    if not data:
        return {"strategy": "No assignments yet. Add your first assignment on the Plan page to get a personalized strategy."}

    summary = "Here are my current assignments:\n"
    for a in data:
        summary += f"- {a['name']}: Effort {a['effort']}/10, Deadline: {a.get('duedate') or 'Not set'}, Tasks: {len(a['tasks'])}\n"

    strategy = googleAIClient.generate_strategy(summary)
    return {"strategy": strategy}

@app.get("/analyze")
def analyze_task(q: str):
    response = googleAIClient.generate_response(q)
    return response

@app.post("/analyze-assignment")
async def analyze_assignment(request: AssignmentRequest):
    # Get the AI response
    response = googleAIClient.generate_response(request.description)

    # Parse the response text as JSON
    assignment_data = json.loads(response.text)

    # Load existing data
    all_data = read_data_from_file()

    # Add id and append
    assignment_data["id"] = len(all_data)
    all_data.append(assignment_data)

    # Save to file
    data_dir = Path("data")
    data_file = data_dir / "data.json"
    with open(data_file, "w") as f:
        json.dump(all_data, f, indent=2)

    return assignment_data
