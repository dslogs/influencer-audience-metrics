import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from PIL import Image

# Load environment variables
load_dotenv()


class ImageAnalysisResponse(BaseModel):
    """Structured response model for image analysis"""
    description: str


api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Load the image
image = Image.open('./analytics.PNG')

response = client.models.generate_content(
    model='gemini-2.0-flash-exp',
    contents=[
        'Please analyze this image',
        image  # PIL Image directly
    ],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=ImageAnalysisResponse
    )
)

result = ImageAnalysisResponse.model_validate_json(response.text)

print(result)