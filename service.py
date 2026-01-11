from google import genai
from dotenv import load_dotenv
load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

GOOGLE_INSTRUCTION = """You must answer in 1 setence starting with "Hello Canh and Tammy". You are an very smart assistant. Your task is to analyze my current tasks and deadlines so that you can help to review this with following criterias:

    - Based on my currents task
"""

class GoogleAIService:
    def generate_response(self, input):
        response = client.models.generate_content(
            model= "gemini-2.5-flash", contents = input,
            config = {
                "system_instruction": GOOGLE_INSTRUCTION
            }
        )
        return response

googleAIClient = GoogleAIService()
response = googleAIClient.generate_response("help me to analyse this task: ")
print(response.text)