# HackathlonApp

An AI-powered study planner. Describe an assignment in plain English and Google
Gemini breaks it down into tasks, estimates effort, extracts the deadline, and
suggests a study strategy. Built with FastAPI and Jinja2 templates.

## Features

- **Analyze assignments** — turn a free-text description into a structured
  breakdown (name, due date, tasks, effort 1–10) using Gemini.
- **Study strategy** — generate 3–5 actionable bullet points from your current
  assignments.
- **Web pages** — Today, Plan, Insights, and Profile views rendered from
  templates.
- Assignments are stored locally in `data/data.json`.

## Requirements

- Python 3.10+
- A Google Gemini API key

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn google-genai python-dotenv pydantic
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

## Running

```bash
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

## API Endpoints

| Method | Path                   | Description                                      |
| ------ | ---------------------- | ------------------------------------------------ |
| GET    | `/`                    | Home page                                        |
| GET    | `/today`               | Today's assignments                              |
| GET    | `/plan`                | Planning view                                    |
| GET    | `/insights`            | Insights page                                    |
| GET    | `/profile`             | Profile page                                     |
| GET    | `/analyze?q=...`       | Analyze a single assignment description          |
| POST   | `/analyze-assignment`  | Analyze a description and save it to `data.json` |
| GET    | `/generate-strategy`   | Generate a study strategy from saved assignments |

## Project Structure

```
main.py            FastAPI app and routes
service.py         Gemini client and response schemas
data/data.json     Saved assignments
templates/         Jinja2 HTML pages
static/            Static assets
```
