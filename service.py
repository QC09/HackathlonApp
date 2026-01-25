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
    name: str = Field(description="The name of the recipe.")
    duedate: Optional[str] = Field(description="Optional time in minutes to prepare the recipe.")
    tasks: List[Task]
    effort: int

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

googleAIClient = GoogleAIService()
# response = googleAIClient.generate_response("My assigment is Economics project, deadline is 2 week from now, I need to create a sample project on micro-economics.")
# print(response.text)