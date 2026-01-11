from google import genai
from dotenv import load_dotenv
load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()


class GoogleAIService:
    def generate_response(self, input):
        response = client.models.generate_content(
            model= "gemini-2.5-flash", contents = input
        )
        return response

googleAIClient = GoogleAIService()
response = googleAIClient.generate_response("help me to analyse this task: ")
print(response.text)