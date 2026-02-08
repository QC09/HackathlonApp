from typing import List, Optional
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

GOOGLE_INSTRUCTION = """You must answer in 1 setence starting with "Hello Canh and Tammy". You are an very smart assistant. Your task is to analyze my current tasks and deadlines so that you can help to review this with following criterias:

    - Based on my current assignment, help me to analyze as my task based on the following criterias:
        - My deadline
        - My effort will be estimate based on sclae from 1-10, for the easy to hard.
    - And help me to suggest my task based on this assignments.
"""

class Task(BaseModel):
    name: str
    description: str

class Summary(BaseModel):
    name: str = Field(description="The name of the assignment.")
    duedate: Optional[str] = Field(default=None, description="The deadline as a date string (e.g. 2026-03-15), or null if not specified.")
    tasks: List[Task]
    effort: int = Field(description="Estimated effort from 1 (easy) to 10 (hard).")

STRATEGY_INSTRUCTION = """You are a study strategy advisor. Based on the student's current assignments and deadlines, create a concise and actionable study strategy. Format your response as 3-5 clear bullet points. Be specific and practical."""

class GoogleAIService:
    def generate_response(self, input):
        response = client.models.generate_content(
            model= "gemini-2.5-flash", contents = input,
            config = {
                "system_instruction": GOOGLE_INSTRUCTION,
                "response_mime_type": "application/json",
                "response_json_schema": Summary.model_json_schema(),
            }
        )
        return response

    def generate_strategy(self, assignments_summary):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=assignments_summary,
            config={
                "system_instruction": STRATEGY_INSTRUCTION,
            }
        )
        return response.text

googleAIClient = GoogleAIService()
# response = googleAIClient.generate_response("My assigment is Economics project, deadline is 2 week from now, I need to create a sample project on micro-economics.")
# print(response.text)