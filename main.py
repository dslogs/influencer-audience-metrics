import os
import functions_framework
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
from flask import jsonify
from at import get_influencer_metric_attachments

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


class TikTokAge(BaseModel):
    quartile_1: float # 18 - 24
    quartile_2: float # 25 - 34
    quartile_3: float # 35 - 44
    quartile_4: float # 45 - 54
    quartile_5: float # 55 + 

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
                '**Output for each quartile field should only be the percentage shown in the image converted to decimal**'
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
    male: float
    female: float

def handle_tt_gender_breakdown(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes))

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            (
                'Output the values in Tik Tok Gender breakdown'
                'ouptut: '
                'male: percentage in photo converted to decimal'
                'female: percentage in photo converted to decimal'
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
    percentage: float

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
                'percentage: the percentage value shown in the image converted to decimal. '
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
    male: float
    female: float

def handle_IG_gender_breakdown(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes))

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            (
                'Output the values in IG Gender breakdown'
                'ouptut: '
                'male: percentage in photo converted to decimal'
                'female: percentage in photo converted to decimal'
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
def main(request):
    data = request.get_json()
    api_key = request.headers.get('X-API-Key')

    if api_key != API_KEY:
        return jsonify({'error' : 'no access'})
    
    record_id = data.get('record')

    if record_id:
        images = get_influencer_metric_attachments(record_id)
        tt_location = None
        if images['tt_location'] is not None:
            tt_location = handle_tt_location_breakdown(images['tt_location'])
        
        tt_gender = None
        if images['tt_gender'] is not None:
            tt_gender = handle_tt_gender_breakdown(images['tt_gender'])
        
        tt_age = None
        if images['tt_age'] is not None:
            tt_age = handle_tt_age_breakdown(images['tt_age'])
        
        # TODO: need to implement all the IG metrics functions
        ig_gender = None
        if images['ig_gender'] is not None:
            ig_gender = handle_IG_gender_breakdown(images['ig_gender'])
        

        return jsonify({
            'tt_location': tt_location.model_dump() if tt_location else None,
            'tt_gender' : tt_gender.model_dump() if tt_gender else None,
            'tt_age' : tt_age.model_dump() if tt_age else None,
            'ig_gender': ig_gender.model_dump() if ig_gender else None
        })


    else:
        return jsonify({ 'error': 'no record' })