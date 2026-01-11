from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()


class GoogleAIService:
    def generate_response(self, input):
        response = client.models.generate_content(
            model= "gemini-2.5-flash", contents = input
        )
        return response
