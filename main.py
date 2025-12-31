import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from PIL import Image

# Load environment variables
load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


class TikTokAge(BaseModel):
    """Structured response model for image analysis"""
    quartile_1: str
    quartile_2: str
    quartile_3: str
    quartile_4: str
    quartile_5: str

def handle_tt_age_breakdown():
    # Load the image
    image = Image.open('./age.jpeg')

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            (
                'Output the values in Tik Tok Age breakdown for each quartile'
                'ouptut: '
                'quartile 1: 18-24'
                'quartile 2: 25-34'
                'quartile 3: 35-44'
                '...etc'
                '**Output for each quartile field should only be the percentage shown in the image**'
            ),
            image
        ],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=TikTokAge
        )
    )

    result = TikTokAge.model_validate_json(response.text)
    print(result)

handle_tt_age_breakdown()