import os
import functions_framework
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
from flask import jsonify

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


class TikTokAge(BaseModel):
    quartile_1: str
    quartile_2: str
    quartile_3: str
    quartile_4: str
    quartile_5: str

def handle_tt_age_breakdown(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes))

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
    return result

class TikTokGender(BaseModel):
    male: str
    female: str

def handle_tt_gender_breakdown(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes))

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            (
                'Output the values in Tik Tok Gender breakdown'
                'ouptut: '
                'male: percentage in photo'
                'female: percentage in photo'
            ),
            image
        ],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=TikTokGender
        )
    )

    result = TikTokGender.model_validate_json(response.text)
    return result

class LocationData(BaseModel):
    country: str
    percentage: str

class TikTokLocation(BaseModel):
    primary: LocationData
    second: LocationData
    third: LocationData
    fourth: LocationData
    other: LocationData

def handle_tt_location_breakdown(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes))

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            (
                'Output the values in Tik Tok Location breakdown. '
                'For each location (primary, second, third, fourth, other), provide structured output with: '
                'country: the country name, '
                'percentage: the percentage value shown in the image. '
                'Primary is the largest country, second is the second largest, etc.'
            ),
            image
        ],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=TikTokLocation
        )
    )

    result = TikTokLocation.model_validate_json(response.text)
    return result

class IGGender(BaseModel):
    male: str
    female: str

def handle_IG_gender_breakdown(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes))

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            (
                'Output the values in IG Gender breakdown'
                'ouptut: '
                'male: percentage in photo'
                'female: percentage in photo'
            ),
            image
        ],
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=IGGender
        )
    )

    result = IGGender.model_validate_json(response.text)
    return result


@functions_framework.http
def tiktok_age_breakdown(request):
    image_bytes = request.get_data()
    result = handle_tt_age_breakdown(image_bytes)
    return jsonify(result.model_dump())


@functions_framework.http
def tiktok_gender_breakdown(request):
    image_bytes = request.get_data()
    result = handle_tt_gender_breakdown(image_bytes)
    return jsonify(result.model_dump())


@functions_framework.http
def tiktok_location_breakdown(request):
    image_bytes = request.get_data()
    result = handle_tt_location_breakdown(image_bytes)
    return jsonify(result.model_dump())


@functions_framework.http
def instagram_gender_breakdown(request):
    image_bytes = request.get_data()
    result = handle_IG_gender_breakdown(image_bytes)
    return jsonify(result.model_dump())